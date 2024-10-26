"""The Urls module.

This module provides the following classes:

- Urls
"""

__all__ = ["Urls"]


from pydantic import HttpUrl

from esak.schemas import BaseModel


class Urls(BaseModel):
    """The Urls object contains commonly used urls.

    Attributes:
        detail: The url for detail information.
        wiki: The url for the wiki entry.
        comiclink:
        reader:
        purchase:
        onsale_date: The url for the on sale date.
        in_app_link:
    """

    detail: HttpUrl
    wiki: HttpUrl | None = None
    comiclink: HttpUrl | None = None
    reader: HttpUrl | None = None
    purchase: HttpUrl | None = None
    onsale_date: HttpUrl | None = None
    in_app_link: HttpUrl | None = None
