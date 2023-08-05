import typing

from py_moysklad.entities.meta_entity import MetaEntity
from py_moysklad.responses.list_entity import ListEntity

if typing.TYPE_CHECKING:
    from py_moysklad.client import ApiClient


class GenericEntityClient:
    entity_class: typing.Type[MetaEntity]
    endpoints: dict

    def __init__(self, api: "ApiClient"):
        self.api = api

    def get_entity_class(self) -> typing.Type[MetaEntity]:
        assert self.entity_class is not None, (
            "'%s' should either include a `entity_class` attribute, "
            "or override the `get_entity_class_class()` method." % self.__class__.__name__
        )

        return self.entity_class

    def get_endpoint(self, endpoint: str) -> str:
        base_url = self.api.host.rstrip("/")
        new_value = str(self.endpoints[endpoint]).lstrip("/")
        return f"{base_url}/{new_value}"


class BaseEndpoint:
    @property
    def client(self):
        api = getattr(self, "api")
        if not api:
            raise Exception()  # FIXME: add custom exception
        return api.client


class RetrieveMixin(BaseEndpoint):
    def get(self, entity_id: str = None):
        if entity_id is None:
            response = self.client.get(endpoint=self.get_endpoint("list"))
            return ListEntity[self.get_entity_class()](**response)
        response = self.client.get(endpoint=self.get_endpoint("retrieve").format(id=entity_id))
        return self.get_entity_class()(**response)


class CreateMixin(BaseEndpoint):
    def create(self, body: dict):
        response = self.client.post(endpoint=self.get_endpoint("create"), body=body)
        return self.get_entity_class()(**response)


class DeleteMixin(BaseEndpoint):
    def delete(self, entity: typing.Union[MetaEntity, int]) -> None:
        if isinstance(entity, MetaEntity):
            entity_id = entity.id
        elif isinstance(entity, int):
            entity_id = entity
        else:
            raise Exception()  # FIXME: add custom exception

        return self.client.delete(endpoint=self.get_endpoint("delete").format(id=entity_id))
