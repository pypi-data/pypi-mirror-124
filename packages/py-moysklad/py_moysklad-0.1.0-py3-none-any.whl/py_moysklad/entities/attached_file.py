import typing
from dataclasses import dataclass
from datetime import datetime

from py_moysklad.entities.attachment import Attachment

if typing.TYPE_CHECKING:
    from py_moysklad.entities.agents.employee import Employee


@dataclass
class AttachedFile(Attachment):
    created: datetime
    createdBy: "Employee"
