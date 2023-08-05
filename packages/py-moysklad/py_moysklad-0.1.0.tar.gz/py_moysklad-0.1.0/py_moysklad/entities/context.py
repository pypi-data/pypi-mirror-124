from pydantic import BaseModel

from py_moysklad.entities.agents.employee import Employee


class Context(BaseModel):
    employee: Employee
