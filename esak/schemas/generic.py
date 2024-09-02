"""The Generic module.

This module provides the following classes:

- GenericItem
- GenericStory
- GenericCreator
"""

from __future__ import annotations

__all__ = ["GenericItem", "GenericStory", "GenericCreator"]

from pydantic import Field, HttpUrl

from esak.schemas.base import BaseModel


class GenericItem(BaseModel):
    """The GenericItem object contains basic information.

    Attributes
    ----------
        id: int

        name: str
            The name of the Generic Item.
        resource_uri: HttpUrl
            The path to the generic resource.
    """

    name: str
    resource_uri: HttpUrl = Field(alias="resourceURI")

    @property
    def id(self) -> int:
        """Pull the id number from the resource_uri.

        Returns
        -------
            The unique ID of the Generic resource.
        """
        return int(self.resource_uri.__str__().split("/")[-1])


class GenericStory(GenericItem):
    """The GenericStory object extends the GenericItem object to include type information.

    Attributes
    ----------
        type: str
            The story type.
    """

    type: str


class GenericCreator(GenericItem):
    """The GenericCreator object extends the GenericItem object to include role information.

    Attributes
    ----------
        role: str
            The role of the creator in the parent entity.
    """

    role: str
