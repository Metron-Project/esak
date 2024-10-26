"""The Creator module.

This module provides the following classes:

- Creator
"""

__all__ = ["Creator"]


from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericItem, GenericStory


class Creator(BaseResource):
    r"""The Creator object contains information for creators.

    Attributes:
        first_name: The first name of the creator.
        middle_name: The middle name of the creator.
        last_name: The last name of the creator.
        suffix: The suffix or honorific for the creator.
        full_name: The full name of the creator (a space-separated concatenation of the
            above four fields).
        comics: A resource list containing the comics which feature work by this creator.
        series: A resource list containing the series which feature work by this creator.
        stories: A resource list containing the stories which feature work by this creator.
        events: A resource list containing the events which feature work by this creator.
    """

    first_name: str
    middle_name: str  # or Blank
    last_name: str
    suffix: str  # or Blank
    full_name: str
    comics: list[GenericItem]
    series: list[GenericItem]
    stories: list[GenericStory]
    events: list[GenericItem]

    @field_validator("comics", "series", "stories", "events", mode="before")
    def map_generic_items(cls, value: dict) -> list[dict]:
        """Convert GenericItems to a list via the 'items' key.

        Args:
            value: Dict of subresource

        Returns:
            List value of the 'items' key
        """
        return value["items"]
