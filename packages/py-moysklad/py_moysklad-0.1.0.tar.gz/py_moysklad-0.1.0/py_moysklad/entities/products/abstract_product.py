from typing import List, Optional

from pydantic import validator

from py_moysklad.entities.assortment import Assortment
from py_moysklad.entities.attached_file import AttachedFile
from py_moysklad.entities.barcode import Barcode
from py_moysklad.entities.price import Price
from py_moysklad.entities.product_folder import ProductFolder
from py_moysklad.entities.uom import Uom


class AbstractProduct(Assortment):
    code: str
    description: str
    vat: int
    effective_vat: int
    # productFolder: ProductFolder
    min_price: Optional[Price]
    buy_price: Price
    sale_prices: List[Price]
    uom: Uom
    barcodes: List[Barcode]
    # files: List[AttachedFile]

    @validator("barcodes", pre=True, always=True)
    def set_barcodes(cls, value, *, values, **kwargs):
        new_value = list()
        for val in value:
            key = list(val.keys())[0]
            value = val[key]
            new_value.append({"type": key.upper(), "value": value})
        return new_value
