from typing import List, Optional

from datetime import datetime

from py_moysklad.entities.agents.agent import Agent
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.cashier import Cashier
from py_moysklad.entities.group import Group
from py_moysklad.entities.image import Image


class Employee(Agent):
    owner: Optional["Employee"]
    shared: Optional[bool]
    lastName: Optional[str]
    externalCode: Optional[str]
    shortFio: Optional[str]
    created: Optional[datetime]
    fullName: Optional[str]
    archived: Optional[bool]
    uid: Optional[str]
    cashiers: Optional[List[Cashier]]
    updated: Optional[datetime]
    email: Optional[str]
    group: Optional[Group]
    description: Optional[str]
    phone: Optional[str]
    firstName: Optional[str]
    middleName: Optional[str]
    attributes: Optional[List[Attribute]]
    image: Optional[Image]
    inn: Optional[str]
    position: Optional[str]
