import re
import sys
import time
import random
import os.path
import logging
import aiohttp
import asyncio
import importlib
from w3lib.url import canonicalize_url
from espider.request import Request
from espider.utils import (
    PriorityQueue, headers_to_dict, cookies_to_dict, get_md5, human_time
)
from espider.response import Response
from inspect import isgenerator
from pprint import pformat
from espider._utils._colorlog import ColoredFormatter
from collections.abc import Iterable, Coroutine

try:
    from redis import Redis
except:
    pass

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(log_color)s%(asctime)s%(reset)s] [%(log_color)s<%(name)s>%(levelname)8s%(reset)s] - %(log_color)s%(message)s%(reset)s'
LOG_DATEFMT = '%Y/%m/%d %H:%M:%S'

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"
]


class Spider(object):

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

        self._msg_total_response = 0
        self._msg_runtime = 0.0
        self._msg_runtime_fmt = ''
        self._msg_items = 0
        self._msg_item_speed = 0
        self._msg_item_dropped = 0
        self._msg_download_speed = 0
        self._msg_request_dropped = 0
        self._msg_response_dropped = 0
        self._msg_yield_item_map = {}
        self._msg_yield_request_map = {}
        self._msg_callback_runtime_map = {}

        self._priority_callback_map = {}
        self._next_priority_index = 1

        self._default_filter_queue = set()
        self._response_filter_code = [404]

        self.LOG_LEVEL = logging.DEBUG
        self.LOG_FORMAT = LOG_FORMAT
        self.LOG_DATEFMT = LOG_DATEFMT

        self.REQUEST_DELAY = 0
        self.REQUEST_WARNING = True
        self.REQUEST_QUEUE = PriorityQueue()
        self.REQUEST_MIDDLEWARES = [self._request_filter]
        self.REQUEST_BATCH_SIZE = 10
        self.REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=600)
        self.REQUEST_CONNECTOR = aiohttp.TCPConnector(limit=100)
        self.REQUEST_SESSION = None

        self.SPIDER_LOOP = asyncio.get_event_loop()
        self.SPIDER_STOP_COUNTDOWN = 3

        self.ITEM_PIPELINES = [self._pipeline]
        self.USER_AGENT_LIST = USER_AGENT_LIST
        self.RESPONSE_MIDDLEWARES = [self._response_filter]

        self.headers = self.headers if hasattr(self, 'headers') else None
        self.cookies = self.cookies if hasattr(self, 'cookies') else {}

        self.logger = logging.getLogger(self.name)
        self._start_time = time.time()

    def start(self):
        try:
            self._load_settings()
            self._init_logger()
            if self.REQUEST_SESSION is None:
                self.REQUEST_SESSION = aiohttp.ClientSession(
                    connector=self.REQUEST_CONNECTOR,
                    timeout=self.REQUEST_TIMEOUT
                )
        except KeyboardInterrupt:
            self.logger.warning('KeyboardInterrupt')
            self._close_msg()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            self.pretty_error(e)
        else:
            self.SPIDER_LOOP.run_until_complete(self._run())

    def _load_settings(self):

        if os.path.exists('settings.py'):
            import settings as st
            for key in self.__dict__.keys() & st.__dict__.keys():
                self.__setattr__(key, st.__dict__.get(key))

            if not self.headers and 'REQUEST_HEADERS' in st.__dict__.keys():
                self.headers = st.__dict__.get('REQUEST_HEADERS')

            if not self.cookies and 'REQUEST_COOKIES' in st.__dict__.keys():
                self.cookies = st.__dict__.get('REQUEST_COOKIES')

    def _init_logger(self):
        self.logger.setLevel(self.LOG_LEVEL or logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(self.LOG_LEVEL or logging.DEBUG)
        formatter = ColoredFormatter(fmt=self.LOG_FORMAT, datefmt=self.LOG_DATEFMT)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    async def _init_queue(self):
        self._msg_callback_runtime_map[self.start_requests.__name__] = (time.time(), 0)
        for r in self.start_requests():
            if not r: continue
            if isinstance(r, tuple) and isinstance(r[1], Request):
                await self.REQUEST_QUEUE.put(r)
                self._update_msg(self.start_requests.__name__)
            else:
                await self._process_item(self.start_requests.__name__, r)

    def _assert_params(self):

        if callable(self.ITEM_PIPELINES):
            self.ITEM_PIPELINES = [self.ITEM_PIPELINES]

        assert isinstance(self.ITEM_PIPELINES, Iterable), \
            'ITEM_PIPELINE type error: except function or function list, get {}.'.format(self.ITEM_PIPELINES)

        for pipe in self.ITEM_PIPELINES:
            assert callable(pipe), 'ITEM_PIPELINE({}) not callable'.format(pipe)

        if self.REQUEST_MIDDLEWARES is not None:
            if callable(self.REQUEST_MIDDLEWARES):
                self.REQUEST_MIDDLEWARES = [self.REQUEST_MIDDLEWARES]
            self._check_middlewares(self.REQUEST_MIDDLEWARES)

        if self.RESPONSE_MIDDLEWARES is not None:
            if callable(self.RESPONSE_MIDDLEWARES):
                self.RESPONSE_MIDDLEWARES = [self.RESPONSE_MIDDLEWARES]
            self._check_middlewares(self.RESPONSE_MIDDLEWARES)

    @staticmethod
    def _check_middlewares(middlewares):
        assert isinstance(middlewares, Iterable), \
            'MIDDLEWARES type error: except function or function list, get {}.'.format(middlewares)
        for mid in middlewares:
            assert callable(mid), 'Middleware {} not callable.'.format(mid)

    async def _run(self):
        """
        主函数
        """
        try:
            self.prepare()
            self._assert_params()
            consumer = asyncio.ensure_future(self._downloader())
            await self._init_queue()
            await self.REQUEST_QUEUE.join()
            consumer.cancel()
            await self.REQUEST_SESSION.close()
        except Exception as e:
            self.pretty_error(e)
            if isinstance(self.REQUEST_SESSION, aiohttp.ClientSession) and not self.REQUEST_SESSION.closed:
                await self.REQUEST_SESSION.close()
            self._close_msg()
        else:
            self._close_msg()

    def request(self, url=None, method=None, data=None, json=None, headers=None, cookies=None, callback=None,
                cb_args=None, cb_kwargs=None, priority=None, allow_redirects=True, **kwargs):
        """
        请求创建函数
        """

        if callback is None: callback = self.parse
        if callback.__name__ not in self._priority_callback_map.keys():
            self._priority_callback_map[callback.__name__] = self._next_priority_index
            self._next_priority_index += 1

        if priority is None: priority = self._priority_callback_map.get(callback.__name__)

        request_params = {
            'url': url,
            'method': method or 'GET',
            'data': data,
            'json': json,
            'headers': headers,
            'cookies': cookies,
            'allow_redirects': allow_redirects,
            **kwargs,
        }
        return priority, Request(**request_params), callback, cb_args or (), cb_kwargs or {}

    async def async_request(self, req, callback, *args, **kwargs):
        """
        异步请求
        """
        # 处理请求
        req = await self._process_request(req)
        if req is None: return

        if self.REQUEST_DELAY: await asyncio.sleep(self.REQUEST_DELAY)

        msg = self._collect_msg(callback.__name__, req)
        self.logger.info(msg)
        # FIXME aiohttp.client_exceptions.ServerDisconnectedError
        try:
            async with self.REQUEST_SESSION.request(**req.__dict__) as _resp:
                data = await _resp.read()
                resp = Response(_resp)
                resp.text = data
                resp.request = req
        except Exception as e:
            self.pretty_error(e)
        else:
            if self.REQUEST_WARNING and resp.status_code != 200:
                detail = pformat(req.__dict__).replace('\n', '\n\t\t')
                detail = re.sub('^\{', '{\n\t\t ', detail)
                detail = re.sub('\}$', '\n\t}', detail)
                msg = msg + ' {}\n\t{}\n'.format(resp.status_code, detail)
                self.logger.warning(msg)

            # 更新爬虫信息
            self._update_msg(callback.__name__)

            # TODO remove 处理响应, 处理回调函数
            # 处理响应
            resp = await self._process_response(resp)
            if resp is None: return

            # 处理回调函数
            await self._process_callback(callback, resp, *args, **kwargs)

    async def _process_request(self, req):

        if not req.headers: req.headers = self.headers or {'User-Agent': random.choice(self.USER_AGENT_LIST)}
        if isinstance(req.headers, str): req.headers = headers_to_dict(req.headers)
        if not req.cookies: req.cookies = self.cookies
        if isinstance(req.cookies, str): req.cookies = cookies_to_dict(req.cookies)
        # 调用请求中间件
        req = await self._process_middleware(req, self.REQUEST_MIDDLEWARES)
        if req is None:
            self._msg_request_dropped += 1
            return
        return req

    async def _process_response(self, resp):
        # 调用响应中间件
        resp = await self._process_middleware(resp, self.RESPONSE_MIDDLEWARES)
        if resp is None:
            self._msg_response_dropped += 1
            return
        return resp

    async def _process_middleware(self, req, middlewares):
        if not middlewares: return req
        try:
            for mid in middlewares:
                req = mid(req)
                if isinstance(req, Coroutine): req = await req
                if not req: return
        except Exception as e:
            self.pretty_error(e)
        else:
            return req

    async def _process_callback(self, callback, resp, *args, **kwargs):
        """
        处理回调函数
        """
        try:
            result = callback(resp, *args, **kwargs)
            if isinstance(result, Coroutine): result = await result
            if not result: return
            if isgenerator(result):
                for r in result:
                    if not r: continue
                    if isinstance(r, tuple) and isinstance(r[1], Request):
                        self.REQUEST_QUEUE.put_nowait(r)
                    else:
                        await self._process_item(callback.__name__, r)
            else:
                await self._process_item(callback.__name__, result)
        except Exception as e:
            self.pretty_error(e)

    async def _process_item(self, cb_name, item):
        """
        处理数据管道
        """
        for pipe in self.ITEM_PIPELINES:
            item = pipe(item)
            if isinstance(item, Coroutine): item = await item
            if item is None:
                self._msg_item_dropped += 1
        # 更新 Item 信息
        self._msg_items += 1
        self._msg_item_speed = self._msg_items / (self._msg_runtime or 1)
        if cb_name not in self._msg_yield_item_map.keys(): self._msg_yield_item_map[cb_name] = 0
        self._msg_yield_item_map[cb_name] += 1

    async def _downloader(self):
        """
        请求调度函数
        """
        while self.SPIDER_STOP_COUNTDOWN >= 0:
            coroutines = []
            if self.REQUEST_BATCH_SIZE != 0:
                if not self.REQUEST_QUEUE.empty():
                    for _ in range(self.REQUEST_BATCH_SIZE):
                        param = self.REQUEST_QUEUE.get_nowait()
                        if not param: continue
                        coroutine = self._create_coroutine(param)
                        coroutines.append(coroutine)
                    await asyncio.gather(*coroutines)
                    self.SPIDER_STOP_COUNTDOWN = 3
                else:
                    self.SPIDER_STOP_COUNTDOWN -= 1
            else:
                if self.REQUEST_QUEUE.empty():
                    self.SPIDER_STOP_COUNTDOWN -= 1
                else:
                    self.SPIDER_STOP_COUNTDOWN = 3
                while not self.REQUEST_QUEUE.empty():
                    coroutine = self._create_coroutine(self.REQUEST_QUEUE.get_nowait())
                    coroutines.append(coroutine)
                await asyncio.gather(*coroutines)

        if hasattr(self.REQUEST_QUEUE, '_finished'):
            self.REQUEST_QUEUE._finished.set()

    def _create_coroutine(self, task_params):
        req, callback, cb_args, cb_kwargs = task_params
        # task = self.SPIDER_LOOP.create_task(
        #     self.async_request(req, callback, *cb_args, **cb_kwargs)
        # )
        # return task
        return self.async_request(req, callback, *cb_args, **cb_kwargs)

    async def _request_filter(self, req):
        url = req.url
        try:
            args = [canonicalize_url(url)]
        except Exception as e:
            self.pretty_error(e)
        else:
            for arg in ('data', 'files', 'auth', 'cert', 'json', 'cookies'):
                if req.__dict__.get(arg):
                    args.append(req.__dict__.get(arg))

            finger = get_md5(*args)

            if finger not in self._default_filter_queue:
                self._default_filter_queue.add(finger)
                return req
            else:
                self.logger.warning("Drop {}".format(req))

    def _response_filter(self, resp):
        if resp.status_code in self._response_filter_code:
            self.logger.warning("Drop {}".format(resp))
        return resp

    def pretty_error(self, err):
        self.logger.error('-' * 100)
        f_max = 0
        funcname = err.__traceback__.tb_frame.f_code.co_name
        lineno = err.__traceback__.tb_lineno
        filepath = err.__traceback__.tb_frame.f_code.co_filename
        if len(funcname) > f_max: f_max = len(funcname)
        if len(err.__class__.__name__) > f_max: f_max = len(err.__class__.__name__)
        e_msgs = [(funcname, filepath, lineno)]

        tb = err.__traceback__
        while tb.tb_next:
            funcname, lineno, filepath = self._get_traceback_info(tb.tb_next)
            if len(funcname) > f_max: f_max = len(funcname)

            e_msgs.append((funcname, filepath, lineno))
            tb = tb.tb_next

        msg_fmt = '{:>%ss} | File "{}", line {}' % f_max
        ctt_fmt = '{:>%ss} | {}' % f_max
        for e_msg in e_msgs:

            content = []
            index = 1
            with open('{}'.format(e_msg[1]), 'r') as f:
                while index <= e_msg[-1] + 1:
                    line = f.readline()
                    if index in [e_msg[-1] - 1, e_msg[-1], e_msg[-1] + 1]:
                        content.append(line.rstrip('\n'))
                    index += 1
            self.logger.error(msg_fmt.format(*e_msg))
            for i, c in enumerate(content):
                if i == 1:
                    self.logger.info(ctt_fmt.format('-->', c))
                else:
                    self.logger.info(ctt_fmt.format('', c))
        for a in err.args:
            self.logger.error(ctt_fmt.format(err.__class__.__name__, a))
            # self.logger.error('{:>s}: {}'.format('ad', a))

        self.logger.error('')

    @staticmethod
    def _get_traceback_info(tb):
        func_name = tb.tb_frame.f_code.co_name
        lineno = tb.f_lineno if hasattr(tb, 'f_lineno') else tb.tb_frame.f_lineno
        filepath = tb.tb_frame.f_code.co_filename
        return func_name, lineno, filepath

    @staticmethod
    def _split_result(result):
        if isinstance(result, (dict, list, str)):
            return result, 1

        if isinstance(result, tuple):
            if len(result) == 1:
                return result[0], 1
            else:
                if isinstance(result[-1], dict):
                    item, *args, kwargs = result
                    return item, args, kwargs, 3
                else:
                    item, *args = result
                    return item, args, 2
        else:
            return result, 1

    def prepare(self):
        pass

    def start_requests(self):
        yield ...

    def parse(self, response, *args, **kwargs):
        pass

    def _pipeline(self, item):
        self.logger.debug('Pipeline: {}'.format(item))
        return item

    def close(self):
        pass

    def _update_msg(self, cb_name):
        current_time = time.time()
        self._msg_runtime = current_time - self._start_time
        self._msg_runtime_fmt = human_time(current_time - self._start_time)
        self._msg_total_response += 1
        self._msg_download_speed = self._msg_total_response / (self._msg_runtime or 1)

        if cb_name not in self._msg_yield_request_map.keys():
            self._msg_yield_request_map[cb_name] = 0
        self._msg_yield_request_map[cb_name] += 1

        if cb_name not in self._msg_callback_runtime_map.keys():
            self._msg_callback_runtime_map[cb_name] = (current_time, 0)

        self._msg_callback_runtime_map[cb_name] = (
            self._msg_callback_runtime_map.get(cb_name)[0], current_time,
            current_time - self._msg_callback_runtime_map.get(cb_name)[0]
        )

    def _collect_msg(self, cb_name, req):

        return '[{}] [R {}/{:.2f}] [I {}/{:.2f}] [{:.2f}] {} {}'.format(
            cb_name,
            self._msg_total_response,
            self._msg_download_speed,
            self._msg_items,
            self._msg_item_speed,
            self._msg_runtime,
            req.__dict__.get('method'),
            req.__dict__.get('url'),
        )

    @property
    def msg(self):
        return {
            'item': self._msg_items,
            'response': self._msg_total_response,
            'runtime': round(self._msg_runtime, 2),
            'callback_runtime': self._msg_callback_runtime_map,
            'yield_item': self._msg_yield_item_map,
            'yield_request': self._msg_yield_request_map,
            'item_speed': round(self._msg_item_speed, 2),
            'download_speed': round(self._msg_download_speed, 2),
            'item_dropped': self._msg_item_dropped,
            'request_dropped': self._msg_request_dropped,
            'response_dropped': self._msg_response_dropped,
        }

    def _close_msg(self):
        try:
            self.close()
        except Exception as e:
            self.pretty_error(e)
        else:
            self.logger.info('')
            title = 'Spider'
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Dropped', {k: v for k, v in self.msg.items() if 'dropped' in k}
            ))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Download', {k: v for k, v in self.msg.items() if k in ['item', 'response']}
            ))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Speed', {k: v for k, v in self.msg.items() if 'speed' in k}
            ))
            self.logger.info('{} - {:21s}: {}'.format(title, 'Yield Item', self._msg_yield_item_map))
            self.logger.info('{} - {:21s}: {}'.format(title, 'Yield Request', self._msg_yield_request_map))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Item Pipelines', [m.__name__ for m in self.ITEM_PIPELINES]
            ))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Request Middlewares', [m.__name__ for m in self.REQUEST_MIDDLEWARES]
            ))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Response Middlewares', [m.__name__ for m in self.RESPONSE_MIDDLEWARES]
            ))
            self.logger.info('{} - {:21s}: {}'.format(
                title, 'Runtime', {
                    'total': self._msg_runtime_fmt,
                    **{k: human_time(v[-1]) for k, v in self._msg_callback_runtime_map.items()}
                }
            ))
            self.logger.info(' Spider Closed '.center(100, '='))


class SpiderManager():
    def __init__(self):
        self.spiders = {}

        self.LOG_LEVEL = LOG_LEVEL
        self.LOG_FORMAT = LOG_FORMAT
        self.LOG_DATEFMT = LOG_DATEFMT

        self.REQUEST_DELAY = None
        self.REQUEST_WARNING = None
        self.REQUEST_QUEUE = None
        self.REQUEST_MIDDLEWARES = None
        self.REQUEST_BATCH_SIZE = None
        self.REQUEST_TIMEOUT = None
        self.REQUEST_CONNECTOR = None
        self.REQUEST_SESSION = None

        self.SPIDER_LOOP = asyncio.get_event_loop()
        self.SPIDER_STOP_COUNTDOWN = None

        self.ITEM_PIPELINES = None
        self.USER_AGENT_LIST = None
        self.RESPONSE_MIDDLEWARES = None

        self.headers = None
        self.cookies = None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.__init_logger()

    def load_spiders(self, path='./spiders'):
        if not os.path.exists(path): return

        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                if root.split('/')[-1].startswith('__'): continue

                py_files = [f for f in files if os.path.splitext(f)[1] == '.py' and not f.startswith('__')]
                if not py_files: continue

                for pf in py_files:
                    module_path = '{}.{}'.format(root.replace('/', '.').strip('.'), os.path.splitext(pf)[0])
                    module = importlib.import_module(module_path)

                    for name, cls in vars(module).items():
                        if not isinstance(cls, type): continue
                        if name == 'Spider' or name.startswith('__'): continue

                        if issubclass(cls, Spider):
                            cls_key = '{}.{}'.format(module_path, cls.__name__)
                            self.spiders[cls_key] = self.__create_spider(cls(), cls_key)
        else:
            self.logger.warning('Load Spiders Error: {} is not a dir'.format(path))

    def __init_logger(self):
        self.logger.setLevel(self.LOG_LEVEL or logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(self.LOG_LEVEL or logging.DEBUG)
        formatter = ColoredFormatter(fmt=self.LOG_FORMAT, datefmt=self.LOG_DATEFMT)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    def __create_spider(self, sp, sp_name=None):
        self.logger.info('Add Spider: {}'.format(sp_name or sp.__class__.__name__))
        return {
            'spider': sp,
            'status': 0
        }

    def add(self, sp):
        if isinstance(sp, type): sp = sp()
        if isinstance(sp, Spider):
            self.spiders[sp.__class__.__name__] = self.__create_spider(sp)
        else:
            self.logger.warning('TypeError: except espider.Spider, get {}'.format(type(sp)))

    def get(self, name=None):
        if not self.spiders: return
        spiders = None

        if name is None:
            spiders = []
            for key, sps in self.spiders.items():
                spiders.append(sps)

        if isinstance(name, str):
            for key, sps in self.spiders.items():
                if key.endswith(name):
                    spiders = sps
        elif isinstance(name, Iterable):
            spiders = []
            for n in name:
                for key, sps in self.spiders.items():
                    if key.endswith(n):
                        spiders.append(sps)
                        break
        return spiders

    def start(self, name=None):
        spiders = self.get(name=name)

        if name is None and not spiders:
            self.logger.error('Spiders map is null')
            return

        if not spiders:
            self.logger.error('Cannot find spider: {}'.format(name))
            return

        if not isinstance(spiders, list):
            spiders = [spiders]

        self.SPIDER_LOOP.run_until_complete(self.__run_spider(spiders))

    async def __run_spider(self, spiders):

        prepared_spider = []
        for sps in spiders:
            sp = sps.get("spider")
            self.logger.info(f' Run Spider {sp.__class__.__name__} '.center(100, '='))
            sps['status'] = 1
            for k, v in self.__dict__.items():
                if v is None: continue
                if k in ['headers', 'cookies']:
                    if not getattr(sp, k):
                        setattr(sp, k, v)
                if k.isupper():
                    setattr(sp, k, v)
            prepared_spider.append(self.__load_spider_config(sp)._run())

        await asyncio.gather(*prepared_spider)

    @staticmethod
    def __load_spider_config(sp):
        try:
            sp._load_settings()
            sp._init_logger()
            if sp.REQUEST_SESSION is None:
                sp.REQUEST_SESSION = aiohttp.ClientSession(
                    connector=sp.REQUEST_CONNECTOR,
                    timeout=sp.REQUEST_TIMEOUT
                )
        except KeyboardInterrupt:
            sp.logger.warning('KeyboardInterrupt')
            sp._close_msg()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            sp.pretty_error(e)
        else:
            return sp
