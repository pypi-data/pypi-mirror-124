from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from py_moysklad.entities.agents.agent import Agent
from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.barcode import Barcode
from py_moysklad.entities.country import Country
from py_moysklad.entities.group import Group
from py_moysklad.entities.image import Image
from py_moysklad.entities.products.abstract_product import AbstractProduct
from py_moysklad.entities.products.good_payment_item_type import GoodPaymentItemType
from py_moysklad.entities.products.good_tax_system import GoodTaxSystem
from py_moysklad.entities.uom import Uom
from py_moysklad.responses.list_entity import ListEntity


class TrackingType(Enum):
    NOT_TRACKED = "NOT_TRACKED"
    TOBACCO = "TOBACCO"
    SHOES = "SHOES"
    LP_CLOTHES = "LP_CLOTHES"
    LP_LINENS = "LP_LINENS"
    PERFUMERY = "PERFUMERY"
    ELECTRONICS = "ELECTRONICS"
    TIRES = "TIRES"
    OTP = "OTP"


class AlcoholEntity(BaseModel):
    excise: bool
    type: int
    strength: Decimal
    volume: Decimal


class ProductPack(BaseModel):
    id: str
    uom: Uom
    quantity: Decimal
    barcodes: Optional[List[Barcode]]


class Product(AbstractProduct):
    owner: Employee
    shared: bool
    group: Group
    # sync_id: str
    updated: datetime
    external_code: str
    archived: bool
    path_name: str
    images: Optional[ListEntity[Image]]
    supplier: Optional[Agent]
    attributes: Optional[List[Attribute]]
    # country: Country
    article: str
    tobacco: Optional[bool]
    weight: Decimal
    volume: Decimal
    packs: Optional[List[ProductPack]]
    alcoholic: Optional[AlcoholEntity]
    variants_count: int
    is_serial_trackable: Optional[bool]
    weighed: Optional[bool]
    things: Optional[List[str]]
    # minimum_balance: Decimal
    # ppe_type: str
    # partial_disposal: bool
    tracking_type: Optional[TrackingType]
    # tnved: str
    # payment_item_type: GoodPaymentItemType
    # tax_system: GoodTaxSystem
