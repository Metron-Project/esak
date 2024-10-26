"""The Story module.

This module provides the following classes:

- Story
"""

__all__ = ["Story"]


from pydantic import field_validator

from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem


class Story(BaseResource):
    r"""The Story object contains information for stories.

    Attributes:
        title: The story title.
        description: A short description of the story.
        type: The story type e.g. interior story, cover, text story.
        creators: A resource list of creators who worked on this story.
        characters: A resource list of characters which appear in this story.
        series: A resource list containing series in which this story appears.
        comics: A resource list containing comics in which this story takes place.
        events: A resource list of the events in which this story appears.
        original_issue: A summary representation of the issue in which this story
            was originally published.
    """

    title: str
    description: str
    type: str
    creators: list[GenericCreator]
    characters: list[GenericItem]
    series: list[GenericItem]
    comics: list[GenericItem]
    events: list[GenericItem]
    original_issue: GenericItem

    @field_validator("creators", "characters", "series", "comics", "events", mode="before")
    def map_generic_items(cls, value: dict) -> list[dict]:
        """Convert GenericItems to a list via the 'items' key.

        Args:
            value: Dict of subresource

        Returns:
            List value of the 'items' key
        """
        return value["items"]
