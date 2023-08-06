import copy
import datetime
import os
import re as _re
import aiohttp
import chardet
import webbrowser
from urllib.parse import urlparse, urlunparse, urljoin
from urllib3.exceptions import (
    DecodeError, ReadTimeoutError, ProtocolError)
from w3lib.encoding import http_content_type_encoding, html_body_declared_encoding

from espider.selector import Selector
from espider.request import Request
from espider._utils._bs4 import UnicodeDammit
from espider._utils._requests import (
    ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError, HTTPError,
    REDIRECT_STATI, codes, CaseInsensitiveDict,
    stream_decode_response_unicode, parse_header_links, iter_slices, guess_json_utf,
    cookiejar_from_dict
)

try:
    import simplejson as json
except ImportError:
    import json

DEFAULT_REDIRECT_LIMIT = 30
CONTENT_CHUNK_SIZE = 10 * 1024
ITER_CHUNK_SIZE = 512

FAIL_ENCODING = "ISO-8859-1"

SPECIAL_CHARACTERS = [
    "[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]"
]

SPECIAL_CHARACTER_PATTERNS = [
    _re.compile(special_character) for special_character in SPECIAL_CHARACTERS
]


def _copy_cookie_jar(jar):
    if jar is None:
        return None

    if hasattr(jar, 'copy'):
        # We're dealing with an instance of RequestsCookieJar
        return jar.copy()
    # We're dealing with a generic CookieJar instance
    new_jar = copy.copy(jar)
    new_jar.clear()
    for cookie in jar:
        new_jar.set_cookie(copy.copy(cookie))
    return new_jar


class Response(object):
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.
    """

    __attrs__ = [
        '_content', 'status_code', 'headers', 'url', 'history',
        'encoding', 'reason', 'cookies', 'elapsed', 'request'
    ]

    def __init__(self, resp=None):
        self._content = False
        self._content_consumed = False
        self._next = None

        #: Integer Code of responded HTTP Status, e.g. 404 or 200.
        self.status_code = None

        #: Case-insensitive Dictionary of Response Headers.
        #: For example, ``headers['content-encoding']`` will return the
        #: value of a ``'Content-Encoding'`` response header.
        self.headers = CaseInsensitiveDict()

        #: File-like object representation of response (for advanced usage).
        #: Use of ``raw`` requires that ``stream=True`` be set on the request.
        #: This requirement does not apply for use internally to Requests.
        self.raw = None

        #: Final URL location of Response.
        self.url = None

        #: Encoding to decode with when accessing r.text.
        self._encoding = None

        #: A list of :class:`Response <Response>` objects from
        #: the history of the Request. Any redirect responses will end
        #: up here. The list is sorted from the oldest to the most recent request.
        self.history = []

        #: Textual reason of responded HTTP Status, e.g. "Not Found" or "OK".
        self.reason = None

        #: A CookieJar of Cookies the server sent back.
        self.cookies = cookiejar_from_dict({})

        #: The amount of time elapsed between sending the request
        #: and the arrival of the response (as a timedelta).
        #: This property specifically measures the time taken between sending
        #: the first byte of the request and finishing parsing the headers. It
        #: is therefore unaffected by consuming the response content or the
        #: value of the ``stream`` keyword argument.
        self.elapsed = datetime.timedelta(0)

        #: The :class:`PreparedRequest <PreparedRequest>` object to which this
        #: is a response.
        self.request = Request()

        # for requests
        self.cost_time = 0
        self.retry_times = 0

        # for selector
        self._cached_selector = None

        # init response content
        if resp:
            attr_map = {
                'status_code': 'status'
            }
            attr_list = ['headers', 'cookies', 'method']
            if isinstance(resp, Response):
                self.__dict__.update(resp.__dict__)
            elif isinstance(resp, aiohttp.client_reqrep.ClientResponse):
                self.__dict__['url'] = resp.url.human_repr()
                for k, v in attr_map.items():
                    if hasattr(resp, v): self.__dict__[k] = resp.__dict__.get(v)
                for a in attr_list:
                    if hasattr(resp, a):
                        self.__dict__[a] = getattr(resp, a)
            else:
                if hasattr(resp, 'text'):
                    self._content = resp.text.encode(chardet.detect(resp.text.encode())['encoding'], errors='replace')

                for k, v in attr_map.items():
                    if hasattr(resp, v): self.__dict__[k] = resp.__dict__.get(v)

        self._cached_text = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __getstate__(self):
        # Consume everything; accessing the content attribute makes
        # sure the content has been fully read.
        if not self._content_consumed:
            self.content

        return {attr: getattr(self, attr, None) for attr in self.__attrs__}

    def __setstate__(self, state):
        for name, value in state.items():
            setattr(self, name, value)

        # pickled objects do not have .raw
        setattr(self, '_content_consumed', True)
        setattr(self, 'raw', None)

    def __repr__(self):
        return '<Response {} {}>'.format(self.url, self.status_code)

    def __bool__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __nonzero__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        try:
            self.raise_for_status()
        except HTTPError:
            return False
        return True

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        return ('location' in self.headers and self.status_code in REDIRECT_STATI)

    @property
    def is_permanent_redirect(self):
        """True if this Response one of the permanent versions of redirect."""
        return ('location' in self.headers and self.status_code in (codes.moved_permanently, codes.permanent_redirect))

    @property
    def next(self):
        """Returns a PreparedRequest for the next request in a redirect chain, if there is one."""
        return self._next

    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the chardet library."""
        return chardet.detect(self.content)['encoding']

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        chunk_size must be of type int or None. A value of None will
        function differently depending on the value of `stream`.
        stream=True will read data as it arrives in whatever size the
        chunks are received. If stream=False, data is returned as
        a single chunk.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """

        def generate():
            # Special case for urllib3.
            if hasattr(self.raw, 'stream'):
                try:
                    for chunk in self.raw.stream(chunk_size, decode_content=True):
                        yield chunk
                except ProtocolError as e:
                    raise ChunkedEncodingError(e)
                except DecodeError as e:
                    raise ContentDecodingError(e)
                except ReadTimeoutError as e:
                    raise ConnectionError(e)
            else:
                # Standard file-like object.
                while True:
                    chunk = self.raw.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

            self._content_consumed = True

        if self._content_consumed and isinstance(self._content, bool):
            raise StreamConsumedError()
        elif chunk_size is not None and not isinstance(chunk_size, int):
            raise TypeError("chunk_size must be an int, it is instead a %s." % type(chunk_size))
        # simulate reading small chunks of the content
        reused_chunks = iter_slices(self._content, chunk_size)

        stream_chunks = generate()

        chunks = reused_chunks if self._content_consumed else stream_chunks

        if decode_unicode:
            chunks = stream_decode_response_unicode(chunks, self)

        return chunks

    def iter_lines(self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=False, delimiter=None):
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.

        .. note:: This method is not reentrant safe.
        """

        pending = None

        for chunk in self.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode):

            if pending is not None:
                chunk = pending + chunk

            if delimiter:
                lines = chunk.split(delimiter)
            else:
                lines = chunk.splitlines()

            if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
                pending = lines.pop()
            else:
                pending = None

            for line in lines:
                yield line

        if pending is not None:
            yield pending

    @property
    def encoding(self):
        """
        编码优先级：自定义编码 > header中编码 > 页面编码 > 根据content猜测的编码
        """
        self._encoding = (
                self._encoding
                or self._headers_encoding()
                or self._body_declared_encoding()
        )
        return self._encoding

    @encoding.setter
    def encoding(self, val):
        self.__clear_cache()
        self._encoding = val

    def __clear_cache(self):
        self.__dict__["_cached_selector"] = None

    def _headers_encoding(self):
        """
        从headers获取头部charset编码
        """
        content_type = self.headers.get("Content-Type") or self.headers.get(
            "content-type"
        )
        if content_type:
            return (
                http_content_type_encoding(content_type) or "utf-8"
                if "application/json" in content_type
                else None
            )

    def _body_declared_encoding(self):
        """
        从html xml等获取<meta charset="编码">
        """

        return html_body_declared_encoding(self.content)

    @property
    def content(self):
        """Content of the response, in bytes."""

        if self._content is False:
            # Read the contents.
            if self._content_consumed:
                raise RuntimeError(
                    'The content for this response was already consumed')

            if self.status_code == 0 or self.raw is None:
                self._content = None
            else:
                self._content = b''.join(self.iter_content(CONTENT_CHUNK_SIZE)) or b''

        self._content_consumed = True
        # don't need to release the connection; that's been handled by urllib3
        # since we exhausted the data.
        return self._content

    @property
    def text(self):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """

        # Try charset from content-type
        encoding = self.encoding

        if not self.content:
            return str('')

        # Fallback to auto-detected encoding.
        if self.encoding is None:
            encoding = self.apparent_encoding

        # Decode unicode from given encoding.
        if self._cached_text is None:
            try:
                self._cached_text = str(self.content, encoding, errors='replace')
                # 补全链接
                self._cached_text = self._absolute_links(self._cached_text)
                # 删除特殊字符
                self._cached_text = self._del_special_character(self._cached_text)
                # 编码矫正
                if self.encoding and self.encoding.upper() == FAIL_ENCODING:
                    content = self._get_unicode_html(self._cached_text)

            except (LookupError, TypeError):
                # A LookupError is raised if the encoding was not found which could
                # indicate a misspelling or similar mistake.
                #
                # A TypeError can be raised if encoding is None
                #
                # So we try blindly encoding.
                self._cached_text = str(self.content, errors='replace')

        return self._cached_text

    @text.setter
    def text(self, text):
        self._cached_text = text
        self._cached_selector = None

    @text.setter
    def text(self, text):
        if isinstance(text, bytes):
            self._content = text
        else:
            self._content = text.encode(chardet.detect(text.encode())['encoding'], errors='replace')

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.

        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises ValueError: If the response body does not contain valid json.
        """

        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using chardet to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return json.loads(
                        self.content.decode(encoding), **kwargs
                    )
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
        return json.loads(self.text, **kwargs)

    @property
    def links(self):
        """Returns the parsed header links of the response, if any."""

        header = self.headers.get('link')

        # l = MultiDict()
        l = {}

        if header:
            links = parse_header_links(header)

            for link in links:
                key = link.get('rel') or link.get('url')
                l[key] = link

        return l

    def raise_for_status(self):
        """Raises :class:`HTTPError`, if one occurred."""

        http_error_msg = ''
        if isinstance(self.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = self.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')
        else:
            reason = self.reason

        if 400 <= self.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (self.status_code, reason, self.url)

        elif 500 <= self.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (self.status_code, reason, self.url)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def close(self):
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
        if not self._content_consumed:
            if self.raw is None: return
            self.raw.close()

        release_conn = getattr(self.raw, 'release_conn', None)
        if release_conn is not None:
            release_conn()

    def _make_absolute(self, link):
        """Makes a given link absolute."""
        try:

            link = link.strip()

            # Parse the link with stdlib.
            parsed = urlparse(link)._asdict()

            # If link is relative, then join it with base_url.
            if not parsed["netloc"]:
                return urljoin(self.url, link)

            # Link is absolute; if it lacks a scheme, add one from base_url.
            if not parsed["scheme"]:
                parsed["scheme"] = urlparse(self.url).scheme

                # Reconstruct the URL to incorporate the new scheme.
                parsed = (v for v in parsed.values())
                return urlunparse(parsed)

        except Exception as e:
            print(
                "Invalid URL <{}> can't make absolute_link. exception: {}".format(
                    link, e
                )
            )

        # Link is absolute and complete with scheme; nothing to be done here.
        return link

    def _absolute_links(self, text):
        regexs = [
            r'(<(?i)a.*?href\s*?=\s*?["\'])(.+?)(["\'])',  # a
            r'(<(?i)img.*?src\s*?=\s*?["\'])(.+?)(["\'])',  # img
            r'(<(?i)link.*?href\s*?=\s*?["\'])(.+?)(["\'])',  # css
            r'(<(?i)script.*?src\s*?=\s*?["\'])(.+?)(["\'])',  # js
        ]

        for regex in regexs:
            def replace_href(text):
                # html = text.group(0)
                link = text.group(2)
                absolute_link = self._make_absolute(link)

                # return re.sub(regex, r'\1{}\3'.format(absolute_link), html) # 使用正则替换，个别字符不支持。如该网址源代码http://permit.mep.gov.cn/permitExt/syssb/xxgk/xxgk!showImage.action?dataid=0b092f8115ff45c5a50947cdea537726
                return text.group(1) + absolute_link + text.group(3)

            text = _re.sub(regex, replace_href, text, flags=_re.S)

        return text

    def _del_special_character(self, text):
        """
        删除特殊字符
        """
        for special_character_pattern in SPECIAL_CHARACTER_PATTERNS:
            text = special_character_pattern.sub("", text)

        return text

    def _get_unicode_html(self, html):
        if not html or not isinstance(html, bytes):
            return html

        converted = UnicodeDammit(html, is_html=True)
        if not converted.unicode_markup:
            raise Exception(
                "Failed to detect encoding of article HTML, tried: %s"
                % ", ".join(converted.tried_encodings)
            )

        html = converted.unicode_markup
        return html

    @property
    def to_dict(self):
        response_dict = {
            "_content": self.content,
            "cookies": self.cookies.get_dict(),
            "encoding": self.encoding,
            "headers": self.headers,
            "status_code": self.status_code,
            "elapsed": self.elapsed.microseconds,  # 耗时
            "url": self.url,
        }

        return response_dict

    @property
    def is_html(self):
        try:
            self.json()
        except:
            return False
        else:
            return True

    @property
    def selector(self):
        if self._cached_selector is None:
            self._cached_selector = Selector(self.text)
        return self._cached_selector

    def find(self, key, data=None, target_type=None):
        return self.selector.find(key=key, data=data, target_type=target_type)

    def find_map(self, map, data=None, target_type=None, **kwargs):
        return self.selector.find_map(map, data=data, target_type=target_type, **kwargs)

    def css(self, query):
        return self.selector.css(query)

    def css_first(self, query, default=''):
        result = self.selector.css(query).extract_first()
        if hasattr(result, 'strip'):
            return default if not result.strip() else result
        else:
            return default if not result else result

    def css_map(self, query_map, one=True):
        return self.selector.css_map(query_map, one=one)

    def xpath(self, query, namespaces=None, **kwargs):
        return self.selector.xpath(query, namespaces=namespaces, **kwargs)

    def xpath_first(self, query, default='', namespaces=None, **kwargs):
        result = self.selector.xpath(query, namespaces=namespaces, **kwargs).extract_first()
        if hasattr(result, 'strip'):
            return default if not result.strip() else result
        else:
            return default if not result else result

    def xpath_map(self, query_map, one=True, namespaces=None, **kwargs):
        return self.selector.xpath_map(query_map, one=one, namespaces=namespaces, **kwargs)

    def re(self, regex, replace_entities=True):
        return self.selector.re(regex, replace_entities=replace_entities)

    def re_map(self, regex_map, one=True, replace_entities=True):
        return self.selector.re_map(regex_map, one=one, replace_entities=replace_entities)

    def re_first(self, regex, default=None, replace_entities=True):
        return self.selector.re_first(regex, default=default, replace_entities=replace_entities)

    def re_map_first(self, regex_map, default=None, replace_entities=True):
        return self.selector.re_map_first(regex_map, default=default, replace_entities=replace_entities)

    def match_map(self, map: dict, one=True, **kwargs):
        return self.selector.match_map(map, one=one, **kwargs)

    def open(self, path=None, save=False):
        self.save_html(path)
        if not path: path = 'index.html'
        webbrowser.open(path)
        if os.path.exists(path) and not save:
            os.remove(path)

    def save_html(self, path=None):
        with open(path or 'index.html', 'w', encoding=self.encoding, errors='replace') as html:
            self.encoding_errors = 'replace'
            html.write(self.text)
            html.flush()

    def save_content(self, path):
        with open(path, 'wb') as html:
            html.write(self.content)
            html.flush()

    def __del__(self):
        self.close()
