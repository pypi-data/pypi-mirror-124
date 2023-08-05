from typing import Optional, Type, TypeVar

from pydantic.generics import GenericModel
from pydantic.main import BaseModel, create_model

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def to_camelcase(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.title() for word in words[1:])


class Entity(GenericModel):
    class Config:
        arbitrary_types_allowed = True
        alias_generator = to_camelcase
