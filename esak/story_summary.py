"""
Story Summary module.

This module provides the following classes:

- StorySummary
- StorySummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class StorySummary:
    """
    The StorySummary object contains basic information for Stories.

    :param `**kwargs`: The keyword arguments used for setting story data from Marvel.
    """

    def __init__(self, id=None, name=None, type=None, resource_uri=None, **kwargs):
        """Intialize a new StorySummary."""
        self.id = id
        self.name = name
        self.type = type
        self.resource_uri = resource_uri
        self.unknown = kwargs


class StorySummarySchema(Schema):
    """Schema for the StorySummary."""

    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")
    type = fields.Str()

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Story Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the StorySummary object.

        :param data: Data from Marvel response.

        :returns: :class:`StorySummary` object
        :rtype: StorySummary
        """
        return StorySummary(**data)
