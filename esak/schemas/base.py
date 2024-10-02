"""The Base module.

This module provides the following classes:

- BaseModel
- BaseResource
"""

__all__ = ["BaseResource", "BaseModel"]

from datetime import datetime

from pydantic import BaseModel as PydanticModel, Field, HttpUrl, field_validator

from esak.schemas.urls import Urls


def to_camel_case(value: str) -> str:
    """Convert attribute name to camelCase.

    Args:
        value: Attribute name

    Returns:
        Value converted to camelCase
    """
    temp = value.replace("_", " ").title().replace(" ", "")
    return temp[0].lower() + temp[1:]


class BaseModel(
    PydanticModel,
    alias_generator=to_camel_case,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="ignore",
):
    """Base model for esak resources."""


class BaseResource(BaseModel):
    r"""Base resource for esak resources.

    Attributes:
        id: The unique ID of the resource.
        modified: The date the resource was most recently modified.
        resource_uri: The canonical URL identifier for this resource.
        thumbnail: The representative image for this resource.
        urls: A set of public website URLs for the resource.
    """

    id: int
    modified: datetime | None = None
    resource_uri: HttpUrl = Field(alias="resourceURI")
    thumbnail: HttpUrl | None = None
    urls: Urls | None = None

    @field_validator("modified", mode="before")
    def check_modified(cls, value: str) -> str | None:
        """Check if modified date starts with '-'.

        Args:
            value: String value of modified

        Returns:
            Input value or None
        """
        return value if value[0] != "-" else None

    @field_validator("thumbnail", mode="before")
    def dict_to_image_url(cls, value: dict[str, str] | None) -> str | None:
        """Convert thumbnail dict into url string.

        Args:
            value: Optional thumbnail object

        Returns:
            String of path + extension or None
        """
        return f"{value['path']}.{value['extension']}" if value else None

    @field_validator("urls", mode="before")
    def map_urls(cls, value: list[dict[str, str]] | None) -> dict[str, str] | None:
        """Convert urls list into a dict.

        Args:
            value: Optional urls list

        Returns:
            Dict of type to url mapped from list or None
        """
        return {x["type"]: x["url"] for x in value} if value else None
