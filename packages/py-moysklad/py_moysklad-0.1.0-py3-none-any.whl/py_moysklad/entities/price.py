from decimal import Decimal
from typing import Optional

from py_moysklad.entities.currency import Currency
from py_moysklad.entities.entity import Entity
from py_moysklad.entities.price_type import PriceType


class Price(Entity):
    price_type: Optional[PriceType]
    currency: Currency
    value: Decimal
