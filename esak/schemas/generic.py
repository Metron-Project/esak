"""The Generic module.

This module provides the following classes:

- GenericItem
- GenericStory
- GenericCreator
"""

__all__ = ["GenericCreator", "GenericItem", "GenericStory"]

from pydantic import Field, HttpUrl

from esak.schemas import BaseModel


class GenericItem(BaseModel):
    """The GenericItem object contains basic information.

    Attributes:
        name: The name of the Generic Item.
        resource_uri: The path to the generic resource.
    """

    name: str
    resource_uri: HttpUrl = Field(alias="resourceURI")

    @property
    def id(self) -> int:
        """Pull the id number from the resource_uri.

        Returns:
            The unique ID of the Generic resource.
        """
        return int(self.resource_uri.__str__().split("/")[-1])


class GenericStory(GenericItem):
    """The GenericStory object extends the GenericItem object to include type information.

    Attributes:
        type: The story type.
    """

    type: str


class GenericCreator(GenericItem):
    """The GenericCreator object extends the GenericItem object to include role information.

    Attributes:
        role: The role of the creator in the parent entity.
    """

    role: str
