"""The Urls module.

This module provides the following classes:

- Urls
"""

from __future__ import annotations

__all__ = ["Urls"]

from pydantic import HttpUrl

from esak.schemas.base import BaseModel


class Urls(BaseModel):
    """The Urls object contains commonly used urls.

    Attributes
    ----------
        detail: HttpUrl
            The url for detail information.
        wiki: HttpUrl | None
            The url for the wiki entry.
        comiclink: HttpUrl | None
        reader: HttpUrl | None
        purchase: HttpUrl | None
        onsale_date: HttpUrl | None
            The url for the on sale date.
        in_app_link: HttpUrl | None
    """

    detail: HttpUrl
    wiki: HttpUrl | None = None
    comiclink: HttpUrl | None = None
    reader: HttpUrl | None = None
    purchase: HttpUrl | None = None
    onsale_date: HttpUrl | None = None
    in_app_link: HttpUrl | None = None
