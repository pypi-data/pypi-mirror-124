from enum import Enum
from typing import Any, Optional

from py_moysklad.entities.meta import Meta
from py_moysklad.entities.meta_entity import MetaEntity


class Type(Enum):
    STRING = "string"
    LONG = "long"
    TIME = "time"
    FILE = "file"
    DOUBLE = "double"
    BOOLEAN = "boolean"
    TEXT = "text"
    LINK = "link"


class Attribute(MetaEntity):
    type: Type
    # private Meta.Type entityType
    value: Optional[Any]
    required: Optional[bool]
    download: Optional[Meta]
    custom_entity_meta: Optional[Meta]
    description: Optional[str]
    # private transient Meta.Type attributeEntityType
