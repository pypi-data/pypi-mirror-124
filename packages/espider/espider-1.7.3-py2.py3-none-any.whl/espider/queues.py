import inspect
from importlib import import_module
from espider.request import Request
from heapq import heappop, heappush

try:
    import cPickle as pickle  # PY2
except ImportError:
    import pickle


class PriorityQueue(object):
    def __init__(self):
        self._queue = []
        self.index = 0

    def push(self, req):
        heappush(self._queue, (-req.priority, self.index, req))
        self.index += 1

    def pop(self):
        return heappop(self._queue)[-1] if self._queue else None

    def empty(self):
        return True if not self._queue else False


class RedisPriorityQueue(object):
    def __init__(self, server, spider):
        self.server = server
        self.key = '{}:{}'.format(spider.name, 'requests')
        self.spider = spider

    @staticmethod
    def loads(s):
        return pickle.loads(s)

    @staticmethod
    def dumps(obj):
        return pickle.dumps(obj, protocol=-1)

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, spider=self.spider)
        return self.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.loads(encoded_request)
        return request_from_dict(obj, spider=self.spider)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request)
        score = -request.priority
        # We don't use zadd method as the order of arguments change depending on
        # whether the class is Redis or StrictRedis, and the option of using
        # kwargs only accepts strings, not bytes.
        self.server.execute_command('ZADD', self.key, score, data)

    def pop(self):
        """
        Pop a request
        """
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])

    def empty(self):
        return self.server.zcard(self.key) == 0

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


def request_to_dict(request, spider=None):
    """Convert Request object to a dict.

    If a spider is given, it will try to find out the name of the spider method
    used in the callback and store that as the callback.
    """
    cb = request.callback
    if callable(cb):
        cb = _find_method(spider, cb)
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': cb,
        'method': request.method,
        'headers': dict(request.headers),
        'data': request.data,
        'cookies': request.cookies,
        'priority': request.priority,
        'cb_kwargs': request.cb_kwargs,
        'cb_args': request.cb_args,
    }
    if type(request) is not Request:
        d['_class'] = request.__module__ + '.' + request.__class__.__name__
    return d


def request_from_dict(d, spider=None):
    """Create Request object from a dict.

    If a spider is given, it will try to resolve the callbacks looking at the
    spider for methods with the same name.
    """
    cb = d['callback']
    if cb and spider:
        cb = _get_method(spider, cb)
    request_cls = load_object(d['_class']) if '_class' in d else Request
    return request_cls(
        url=to_unicode(d['url']),
        callback=cb,
        method=d['method'],
        headers=d['headers'],
        data=d['data'],
        cookies=d['cookies'],
        priority=d['priority'],
        cb_kwargs=d.get('cb_kwargs'),
        cb_args=d.get('cb_args'),
    )


def to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of a bytes object ``text``. If
    ``text`` is already an unicode object, return it as-is."""
    if isinstance(text, str):
        return text
    if not isinstance(text, (bytes, str)):
        raise TypeError('to_unicode must receive a bytes or str '
                        f'object, got {type(text).__name__}')
    if encoding is None:
        encoding = 'utf-8'
    return text.decode(encoding, errors)


def load_object(path):
    """Load an object given its absolute object path, and return it.

    The object can be the import path of a class, function, variable or an
    instance, e.g. 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'.

    If ``path`` is not a string, but is a callable object, such as a class or
    a function, then return it as is.
    """

    if not isinstance(path, str):
        if callable(path):
            return path
        else:
            raise TypeError("Unexpected argument type, expected string "
                            "or object, got: %s" % type(path))

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError(f"Error loading object '{path}': not a full path")

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError(f"Module '{module}' doesn't define any object named '{name}'")

    return obj


def _find_method(obj, func):
    # Only instance methods contain ``__func__``
    if obj and hasattr(func, '__func__'):
        members = inspect.getmembers(obj, predicate=inspect.ismethod)
        for name, obj_func in members:
            if obj_func.__func__ is func.__func__:
                return name
    raise ValueError(f"Function {func} is not an instance method in: {obj}")


def _get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        raise ValueError(f"Method {name!r} not found in: {obj}")
