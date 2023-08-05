from dataclasses import dataclass

from py_moysklad.entities.meta import Meta
from py_moysklad.entities.meta_entity import MetaEntity


@dataclass
class Attachment(MetaEntity):
    title: str
    filename: str
    content: str
    size: int
    miniature: Meta
    tiny: Meta
