from typing import Union

import httpx
from urllib.parse import urljoin


class HTTP:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(
        self,
        *,
        token: str,
        host: str = "https://online.moysklad.ru/",
        timeout: int = 60,
    ):
        self.host = host
        self.token = token
        self.timeout = timeout

    def _request(
        self,
        *,
        method: str,
        url: str,
        params: dict = None,
        json: dict = None,
    ) -> Union[dict, bytes]:
        url = url.strip("/")
        url = urljoin(self.host, url)
        self.headers["Authorization"] = f"Bearer {self.token}"

        params = {
            "method": method,
            "url": url,
            "headers": self.headers,
            "timeout": self.timeout,
            "params": params,
        }

        if json:
            params["json"] = json

        response = httpx.request(**params)

        return response.json()

    def get(self, url: str):
        return self._request(method="get", url=url)

    def post(self, url: str, params: dict = None, json: dict = None):
        return self._request(method="post", url=url, params=params, json=json)
