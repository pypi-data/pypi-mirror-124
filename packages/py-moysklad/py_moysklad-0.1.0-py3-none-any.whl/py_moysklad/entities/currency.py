from decimal import Decimal
from typing import Optional

from py_moysklad.entities.meta_entity import MetaEntity


class Currency(MetaEntity):
    full_name: Optional[str]
    rate: Optional[Decimal]
    # private MultiplicityType multiplicity;
    # private UpdateType rateUpdateType;
    indirect: Optional[bool]
    code: Optional[str]
    isoCode: Optional[str]
    system: Optional[bool]
    # private Unit majorUnit;
    # private Unit minorUnit;
    archived: Optional[bool]
