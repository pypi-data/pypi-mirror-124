import typing
from dataclasses import dataclass

from py_moysklad.entities.meta_entity import MetaEntity

if typing.TYPE_CHECKING:
    from py_moysklad.entities.agents.employee import Employee


@dataclass
class Cashier(MetaEntity):
    employee: "Employee"
    # private RetailStore retailStore;
