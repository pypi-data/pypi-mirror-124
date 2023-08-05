import typing

from py_moysklad.clients.product_client import ProductClient

if typing.TYPE_CHECKING:
    from py_moysklad.client import ApiClient


class EntityClient:
    def __init__(self, api: "ApiClient"):
        self.api = api

    def product(self) -> ProductClient:
        return ProductClient(self.api)
