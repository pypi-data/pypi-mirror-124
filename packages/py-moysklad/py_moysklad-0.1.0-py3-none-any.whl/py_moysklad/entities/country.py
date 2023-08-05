from dataclasses import dataclass
from datetime import datetime

from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.group import Group
from py_moysklad.entities.meta_entity import MetaEntity


@dataclass
class Country(MetaEntity):
    external_code: str
    updated: datetime
    description: str
    code: str
    owner: Employee
    shared: bool
    group: Group
