from typing import List

from py_moysklad.entities.meta_entity import MetaEntity


class Discount(MetaEntity):
    active: bool
    allAgents: bool
    agentTags: List[str]
