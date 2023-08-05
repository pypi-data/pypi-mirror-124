from typing import Generic, List, Optional, TypeVar

from py_moysklad.entities.context import Context
from py_moysklad.entities.meta_entity import MetaEntity


T = TypeVar("T", bound=MetaEntity)


class ListEntity(MetaEntity, Generic[T]):
    context: Optional[Context]
    rows: Optional[List[T]]
