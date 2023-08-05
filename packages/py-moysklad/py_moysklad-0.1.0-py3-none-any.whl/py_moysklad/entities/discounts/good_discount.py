from typing import List

from py_moysklad.entities.discounts.discount import Discount


class GoodDiscount(Discount):
    allProducts: bool
    assortment: List[ProductMarker]
    productFolders: List[ProductFolder]
