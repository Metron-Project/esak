"""The Event module.

This module provides the following classes:

- Event
"""

from __future__ import annotations

__all__ = ["Event"]
from datetime import date, datetime

from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Event(BaseResource):
    r"""The Event object contains information for events.

    Attributes
    ----------
        title: str
            The title of the event.
        description: str
            A description of the event.
        start: date | None
            The date of publication of the first issue in this event.
        end: date | None
            The date of publication of the last issue in this event.
        creators: list[GenericCreator]
            A resource list containing creators whose work appears in this event.
        characters: list[GenericItem]
            A resource list containing the characters which appear in this event.
        stories: list[GenericStory]
            A resource list containing the stories in this event.
        comics: list[GenericItem]
            A resource list containing the comics in this event.
        series: list[GenericItem]
            A resource list containing the series in this event.
        next: GenericItem | None
            A summary representation of the event which follows this event.
        previous: GenericItem | None
            A summary representation of the event which preceded this event.
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

        Parameters
        ----------
            value: str | None
                String value to parse as date

        Returns
        -------
            Parsed date or None
        """
        if value:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date()
        return None

    @field_validator("creators", "characters", "stories", "comics", "series", mode="before")
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
