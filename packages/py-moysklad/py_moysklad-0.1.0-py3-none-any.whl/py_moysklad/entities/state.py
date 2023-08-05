from dataclasses import dataclass
from datetime import datetime
from typing import List

from py_moysklad.entities.address import Address
from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.group import Group
from py_moysklad.entities.meta_entity import MetaEntity


@dataclass
class State(MetaEntity):
    color: int
    # private StateType stateType;
    # private Meta.Type entityType;
