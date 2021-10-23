"""
Creator Summary module.

This module provides the following classes:

- CreatorSummary
- CreatorSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class CreatorSummary:
    """
    The CreatorSummary object contains basic information for creators.

    :param `**kwargs`: The keyword arguments used for getting creator data from Marvel.
    """

    def __init__(self, id=None, name=None, role=None, resource_uri=None, **kwargs):
        """Intialize a new CreatorSummary."""
        self.id = id
        self.name = name
        self.role = role
        self.resource_uri = resource_uri
        self.unknown = kwargs


class CreatorSummarySchema(Schema):
    """Schema for the CreatorSummary."""

    id = fields.Int()
    name = fields.Str()
    role = fields.Str()
    resourceURI = fields.Url(attribute="resource_uri")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Creator Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the CreatorSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`CreatorSummary` object
        :rtype: CreatorSummary
        """
        return CreatorSummary(**data)
