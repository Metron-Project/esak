"""The Character module.

This module provides the following classes:

- Character
"""

__all__ = ["Character"]

from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericItem, GenericStory


class Character(BaseResource):
    r"""The Character object contains information for characters.

    Attributes:
        name: The name of the character.
        description: A short bio or description of the character.
        comics: A resource list containing comics which feature this character.
        series: A resource list of series in which this character appears.
        stories: A resource list of stories in which this character appears.
        events: A resource list of events in which this character appears.
    """

    name: str
    description: str
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
