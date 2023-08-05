from typing import Optional

from pydantic import BaseModel

from py_moysklad.entities.entity import to_camelcase


class Meta(BaseModel):
    href: Optional[str]
    metadata_href: Optional[str]
    type: Optional[str]  # noqa: VNE003, FIXME: ENUM
    media_type: Optional[str]
    uuid_href: Optional[str]
    size: Optional[int]
    limit: Optional[int]
    offset: Optional[int]

    class Config:
        alias_generator = to_camelcase
