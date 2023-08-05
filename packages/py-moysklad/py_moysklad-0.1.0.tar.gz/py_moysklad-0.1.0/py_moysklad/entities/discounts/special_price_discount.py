from decimal import Decimal

from py_moysklad.entities.discounts.good_discount import GoodDiscount
from py_moysklad.entities.meta_entity import MetaEntity


class SpecialPriceDiscount(GoodDiscount):
    usePriceType: bool
    specialPrice: "SpecialPriceData"
    discount: Decimal

    class SpecialPriceData(MetaEntity):
        value: int
        priceType: PriceType
