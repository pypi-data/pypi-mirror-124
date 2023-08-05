from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.group import Group
from py_moysklad.entities.meta_entity import MetaEntity


class Uom(MetaEntity):
    updated: Optional[datetime]
    description: Optional[str]
    code: Optional[str]
    external_code: Optional[str]
    shared: Optional[bool]
    owner: Optional[Employee]
    group: Optional[Group]
