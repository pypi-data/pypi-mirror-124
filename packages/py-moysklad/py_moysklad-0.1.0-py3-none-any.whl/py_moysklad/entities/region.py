from dataclasses import dataclass
from datetime import datetime


@dataclass
class Region:
    updated: datetime
    code: str
    external_code: str
