"""The Series module.

This module provides the following classes:

- Series
"""

from __future__ import annotations

__all__ = ["Series"]

from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Series(BaseResource):
    """The Series object contains information for a series.

    Attributes
    ----------
        title: str
            The canonical title of the series.
        description: str | None
            A description of the series.
        start_year: int
            The first year of publication for the series.
        end_year: int
            The last year of publication for the series (conventionally, 2099 for ongoing series).
        rating: str
            The age-appropriateness rating for the series.
        type: str
        creators: list[GenericCreator]
            A resource list of creators whose work appears in comics in this series.
        characters: list[GenericItem]
            A resource list containing characters which appear in comics in this series.
        stories: list[GenericStory]
            A resource list containing stories which occur in comics in this series.
        comics: list[GenericItem]
            A resource list containing comics in this series.
        events: list[GenericItem]
            A resource list containing events which take place in comics in this series.
        next: GenericItem | None
            A summary representation of the series which follows this series.
        previous: GenericItem | None
            A summary representation of the series which preceded this series.
    """

    title: str
    description: str | None = None
    start_year: int
    end_year: int
    rating: str  # or Blank
    type: str  # or Blank
    creators: list[GenericCreator]
    characters: list[GenericItem]
    stories: list[GenericStory]
    comics: list[GenericItem]
    events: list[GenericItem]
    next: GenericItem | None = None
    previous: GenericItem | None = None

    @field_validator("creators", "characters", "stories", "comics", "events", mode="before")
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
