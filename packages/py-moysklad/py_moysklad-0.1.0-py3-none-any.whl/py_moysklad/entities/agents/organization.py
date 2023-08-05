from typing import List

from datetime import datetime

from py_moysklad.entities.address import Address
from py_moysklad.entities.agents.agent import Agent
from py_moysklad.entities.agents.employee import Employee
from py_moysklad.entities.attribute import Attribute
from py_moysklad.entities.group import Group


class Organization(Agent):
    syncId: str
    owner: Employee
    shared: bool
    group: Group
    updated: datetime
    description: str
    code: str
    externalCode: str
    archived: bool
    created: datetime
    # private CompanyType companyType;
    legalTitle: str
    email: str
    # private ListEntity<AgentAccount> accounts;
    isEgaisEnable: bool
    payerVat: bool
    director: str
    chiefAccountant: str
    legalAddress: str
    legalAddressFull: Address
    inn: str
    kpp: str
    ogrn: str
    ogrnip: str
    okpo: str
    certificateNumber: str
    certificateDate: datetime
    attributes: List[Attribute]
    phone: str
    fax: str
    fsrarId: str
    utmUrl: str
    actualAddress: str
    actualAddressFull: Address
    trackingContractNumber: str
    trackingContractDate: datetime
    # private BonusProgram bonusProogram;
    bonusPoints: int
