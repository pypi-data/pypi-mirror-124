from datetime import datetime
from decimal import Decimal
from typing import List

from py_moysklad.entities.address import Address
from py_moysklad.entities.agents.agent import Agent
from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.discounts.discount import Discount
from py_moysklad.entities.group import Group
from py_moysklad.entities.price_type import PriceType
from py_moysklad.entities.state import State


class Counterparty(Agent):
    owner: Employee
    shared: bool
    code: str
    group: Group
    syncId: str
    updated: datetime
    description: str
    externalCode: str
    archived: bool
    created: datetime
    # private CompanyType companyType;
    legalTitle: str
    legalAddress: str
    legalAddressFull: Address
    inn: str
    kpp: str
    ogrn: str
    ogrnip: str
    okpo: str
    certificateNumber: str
    certificateDate: datetime
    email: str
    phone: str
    fax: str
    actualAddress: str
    actualAddressFull: Address
    # private ListEntity<AgentAccount> accounts;
    tags: List[str]
    discounts: List["DiscountData"]
    # private ListEntity<ContactPerson> contactpersons;
    # private ListEntity<Note> notes;
    discountCardNumber: str
    state: State
    salesAmount: int
    attributes: List[Attribute]
    priceType: PriceType

    class DiscountData:
        discount: Discount
        personalDiscount: Decimal
        demandSumCorrection: Decimal
