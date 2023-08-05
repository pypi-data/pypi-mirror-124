from enum import Enum
from typing import Optional


from py_moysklad.entities.meta_entity import MetaEntity


class Type(Enum):
    EAN13 = "EAN13"
    EAN8 = "EAN8"
    CODE128 = "CODE128"
    GTIN = "GTIN"
    UPC = "UPC"


class Barcode(MetaEntity):
    type: Optional[Type]
    value: Optional[str]
