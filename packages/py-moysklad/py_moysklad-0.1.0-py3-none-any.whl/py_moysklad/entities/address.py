from dataclasses import dataclass

from py_moysklad.entities.country import Country
from py_moysklad.entities.region import Region


@dataclass
class Address:
    postal_code: str
    country: Country
    region: Region
    city: str
    street: str
    house: str
    apartment: str
    add_info: str
    comment: str
