"""The Event module.

This module provides the following classes:

- Event
"""

__all__ = ["Event"]
from datetime import date, datetime

from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Event(BaseResource):
    r"""The Event object contains information for events.

    Attributes:
        title: The title of the event.
        description: A description of the event.
        start: The date of publication of the first issue in this event.
        end: The date of publication of the last issue in this event.
        creators: A resource list containing creators whose work appears in this event.
        characters: A resource list containing the characters which appear in this event.
        stories: A resource list containing the stories in this event.
        comics: A resource list containing the comics in this event.
        series: A resource list containing the series in this event.
        next: A summary representation of the event which follows this event.
        previous: A summary representation of the event which preceded this event.
    """

    title: str
    description: str
    start: date | None = None
    end: date | None = None
    creators: list[GenericCreator]
    characters: list[GenericItem]
    stories: list[GenericStory]
    comics: list[GenericItem]
    series: list[GenericItem]
    next: GenericItem | None = None
    previous: GenericItem | None = None

    @field_validator("start", "end", mode="before")
    def datetime_to_date(cls, value: str | None) -> date | None:
        """Convert optional string to date.

        Args:
            value: String value to parse as date

        Returns:
            Parsed date or None
        """
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date() if value else None

    @field_validator("creators", "characters", "stories", "comics", "series", mode="before")
    def map_generic_items(cls, value: dict) -> list[dict]:
        """Convert GenericItems to a list via the 'items' key.

        Args:
            value: Dict of subresource

        Returns:
            List value of the 'items' key
        """
        return value["items"]
