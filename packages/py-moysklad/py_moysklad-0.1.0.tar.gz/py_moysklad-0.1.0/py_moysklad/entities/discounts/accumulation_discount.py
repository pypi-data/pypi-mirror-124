from decimal import Decimal
from typing import List

from py_moysklad.entities.discounts.good_discount import GoodDiscount


class AccumulationDiscount(GoodDiscount):
    levels: List["AccumulationLevel"]

    class AccumulationLevel:
        amount: Decimal
        discount: Decimal
