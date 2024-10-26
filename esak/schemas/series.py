"""The Series module.

This module provides the following classes:

- Series
"""

__all__ = ["Series"]


from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Series(BaseResource):
    """The Series object contains information for a series.

    Attributes:
        title: The canonical title of the series.
        description: A description of the series.
        start_year: The first year of publication for the series.
        end_year: The last year of publication for the series
            (conventionally, 2099 for ongoing series).
        rating: The age-appropriateness rating for the series.
        type:
        creators: A resource list of creators whose work appears in comics in this series.
        characters: A resource list containing characters which appear in comics in this series.
        stories: A resource list containing stories which occur in comics in this series.
        comics: A resource list containing comics in this series.
        events: A resource list containing events which take place in comics in this series.
        next: A summary representation of the series which follows this series.
        previous: A summary representation of the series which preceded this series.
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

        Args:
            value: Dict of subresource

        Returns:
            List value of the 'items' key
        """
        return value["items"]
