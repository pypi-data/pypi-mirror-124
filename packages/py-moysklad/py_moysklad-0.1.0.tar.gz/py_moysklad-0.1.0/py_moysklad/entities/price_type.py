from dataclasses import dataclass

from py_moysklad.entities.meta_entity import MetaEntity


class PriceType(MetaEntity):
    external_code: str
