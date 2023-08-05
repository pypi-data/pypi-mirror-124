from typing import Optional

from py_moysklad.entities.entity import Entity
from py_moysklad.entities.meta import Meta


class MetaEntity(Entity):
    id: Optional[str]  # noqa: VNE003
    account_id: Optional[str]
    name: Optional[str]
    meta: Optional[Meta]
