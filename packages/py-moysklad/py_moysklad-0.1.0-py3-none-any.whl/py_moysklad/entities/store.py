from dataclasses import dataclass
from datetime import datetime
from typing import List

from py_moysklad.entities.address import Address
from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.group import Group
from py_moysklad.entities.meta_entity import MetaEntity


@dataclass
class Store(MetaEntity):
    owner: Employee
    shared: bool
    group: Group
    updated: datetime
    description: str
    code: str
    externalCode: str
    archived: bool
    address: str
    addressFull: Address
    parent: "Store"
    pathName: str
    attributes: List[Attribute]
