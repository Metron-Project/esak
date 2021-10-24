"""
Character Summary module.

This module provides the following classes:

- CharacterSummary
- CharacterSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class CharacterSummary:
    """
    The CharacterSummary object contains basic information for Characters.

    :param `**kwargs`: The keyword arguments used for getting character data from Marvel.
    """

    def __init__(self, id=None, name=None, role=None, resource_uri=None, **kwargs):
        """Intialize a new CharacterSummary."""
        self.id = id
        self.name = name
        self.role = role
        self.resource_uri = resource_uri
        self.unknown = kwargs


class CharacterSummarySchema(Schema):
    """Schema for the CharacterSummary."""

    id = fields.Int()
    name = fields.Str()
    role = fields.Str()
    resourceURI = fields.Url(attribute="resource_uri")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Character Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the CharacterSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`CharacterSummary` object
        :rtype: CharacterSummary
        """
        return CharacterSummary(**data)
