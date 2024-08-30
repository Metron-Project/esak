"""The Base module.

This module provides the following classes:

- BaseResource
"""

from __future__ import annotations

__all__ = ["BaseResource"]

from datetime import datetime

from pydantic import Field, HttpUrl, field_validator

from esak.schemas import BaseModel
from esak.schemas.urls import Urls


class BaseResource(BaseModel):
    r"""Base resource for esak resources.

    Attributes
    ----------
        id: int
            The unique ID of the resource.
        modified: datetime | None
            The date the resource was most recently modified.
        resource_uri: HttpUrl
            The canonical URL identifier for this resource.
        thumbnail: HttpUrl | None
            The representative image for this resource.
        urls: Urls
            A set of public website URLs for the resource.
    """

    id: int
    modified: datetime | None = None
    resource_uri: HttpUrl = Field(alias="resourceURI")
    thumbnail: HttpUrl | None = None
    urls: Urls | None = None

    @field_validator("modified", mode="before")
    def check_modified(cls, value: str) -> str | None:
        """Check if modified date starts with '-'.

        Parameters
        ----------
            value: str
                String value of modified

        Returns
        -------
            input value or None
        """
        if value[0] == "-":
            return None
        return value

    @field_validator("thumbnail", mode="before")
    def dict_to_image_url(cls, value: dict[str, str] | None) -> str | None:
        """Convert thumbnail dict into url string.

        Parameters
        ----------
            value: dict[str, str] | None
                Optional thumbnail object

        Returns
        -------
            String of path + extension or None
        """
        if value:
            return f"{value['path']}.{value['extension']}"
        return None

    @field_validator("urls", mode="before")
    def map_urls(cls, value: list[dict[str, str]] | None) -> dict[str, str] | None:
        """Convert urls list into a dict.

        Parameters
        ----------
            value: list[dict[str, str]] | None
                Optional urls list

        Returns
        -------
            Dict of type to url mapped from list or None
        """
        if value:
            return {x["type"]: x["url"] for x in value}
        return None
