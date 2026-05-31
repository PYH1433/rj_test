from utils.request_util import Request, host
from utils.yaml_util import read_yaml
from utils.logger_utils import Logger


class BaseApi:
    _token_cache = None

    def __init__(self):
        self.request = Request()
        self.logger = Logger.getlog()

    @property
    def _host(self):
        return host.rstrip("/")

    def _get_token(self):
        if BaseApi._token_cache is None:
            try:
                BaseApi._token_cache = read_yaml("data.yaml", "user_token_header")
            except (KeyError, FileNotFoundError, TypeError):
                return None
        return BaseApi._token_cache

    def _set_token(self, token):
        BaseApi._token_cache = token

    def _get_headers(self, extra_headers=None):
        headers = {}
        token = self._get_token()
        if token:
            headers["User-Token"] = token
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _build_url(self, endpoint):
        endpoint = endpoint.lstrip("/")
        return f"{self._host}/{endpoint}"

    def get(self, endpoint, no_auth=False, **kwargs):
        url = self._build_url(endpoint)
        extra_headers = kwargs.pop("headers", None)
        headers = extra_headers or {} if no_auth else self._get_headers(extra_headers)
        return self.request.get(url, headers=headers, **kwargs)

    def post(self, endpoint, no_auth=False, **kwargs):
        url = self._build_url(endpoint)
        extra_headers = kwargs.pop("headers", None)
        headers = extra_headers or {} if no_auth else self._get_headers(extra_headers)
        return self.request.post(url, headers=headers, **kwargs)
