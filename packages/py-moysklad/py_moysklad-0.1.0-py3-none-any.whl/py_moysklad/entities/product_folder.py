from dataclasses import dataclass
from datetime import datetime

from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.group import Group
from py_moysklad.entities.meta_entity import MetaEntity
from py_moysklad.entities.products.good_tax_system import GoodTaxSystem


class ProductFolder(MetaEntity):
    owner: Employee
    pathName: str
    shared: bool
    archived: bool
    code: str
    externalCode: str
    description: str
    productFolder: "ProductFolder"
    updated: datetime
    group: Group
    vat: int
    effectiveVat: int
    taxSystem: GoodTaxSystem
