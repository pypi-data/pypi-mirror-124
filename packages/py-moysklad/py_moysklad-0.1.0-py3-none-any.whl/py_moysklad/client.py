from apiclient import APIClient as HTTPClient, HeaderAuthentication, JsonRequestFormatter, JsonResponseHandler

from py_moysklad.clients.entity_client import EntityClient


class ApiClient:
    def __init__(self, token: str, client: HTTPClient, host: str = "online.moysklad.ru"):
        self.host = host
        self.token = token
        self.client = client

    @classmethod
    def create_with_bearer_token(cls, host: str, token: str) -> "ApiClient":
        api_client = cls(host=host, token=token, client=cls.create_http_client())
        api_client.set_token(token=token)
        return api_client

    @classmethod
    def create_http_client(cls) -> HTTPClient:
        return HTTPClient(response_handler=JsonResponseHandler, request_formatter=JsonRequestFormatter)

    def set_token(self, token):
        self.client.set_authentication_method(authentication_method=HeaderAuthentication(token=token))

    def entity(self) -> EntityClient:
        return EntityClient(self)
