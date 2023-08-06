from espider.utils import headers_to_dict, cookies_to_dict


class Request:
    def __init__(self, **kwargs):
        self.url = None
        self.method = None
        self.data = None
        self.json = None
        self.headers = None
        self.cookies = None
        self.allow_redirects = None
        self.priority = None
        self.callback = None
        self.cb_args = None
        self.cb_kwargs = None
        self.__dict__.update(kwargs)

        if self.cb_args is None: self.cb_args = ()
        if self.cb_kwargs is None: self.cb_kwargs = {}

        if isinstance(self.headers, str): self.headers = headers_to_dict(self.headers)
        if isinstance(self.cookies, str): self.cookies = cookies_to_dict(self.cookies)

    def __repr__(self):
        return '<Request {}>'.format(self.url)
