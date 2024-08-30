"""esak.schemas package entry file.

This module provides the following classes:

- BaseModel
"""

__all__ = ["BaseModel"]

from pydantic import BaseModel as PydanticModel


def to_camel_case(value: str) -> str:
    temp = value.replace("_", " ").title().replace(" ", "")
    return temp[0].lower() + temp[1:]


class BaseModel(
    PydanticModel,
    alias_generator=to_camel_case,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    # extra="ignore",
    extra="forbid",
):
    """Base model for esak resources."""
