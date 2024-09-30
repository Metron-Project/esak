"""The Character module.

This module provides the following classes:

- Character
"""

from __future__ import annotations

__all__ = ["Character"]

from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericItem, GenericStory


class Character(BaseResource):
    r"""The Character object contains information for characters.

    Attributes
    ----------
        name: str
            The name of the character.
        description: str
            A short bio or description of the character.
        comics: list[GenericItem]
            A resource list containing comics which feature this character.
        series: list[GenericItem]
            A resource list of series in which this character appears.
        stories: list[GenericStory]
            A resource list of stories in which this character appears.
        events: list[GenericItem]
            A resource list of events in which this character appears.
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

        Parameters
        ----------
            value: dict
                Dict of subresource

        Returns
        -------
            List value of the 'items' key
        """
        return value["items"]
