"""
Generic Summary module.

This module provides the following classes:

- GenericSummary
- GenericSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class GenericSummary:
    """
    The GenericSummary object contains basic information.

    :param `**kwargs`: The keyword arguments used for getting data from Marvel.
    """

    def __init__(self, id=None, name=None, resource_uri=None, type=None, role=None, **kwargs):
        """Intialize a new GenericSummary."""
        self.id = id
        self.name = name
        self.resource_uri = resource_uri
        self.type = type
        self.role = role
        self.unknown = kwargs


class GenericSummarySchema(Schema):
    """Schema for the GenericSummary."""

    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")
    type = fields.Str()
    role = fields.Str()

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the GenericSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`GenericSummary` object
        :rtype: GenericSummary
        """
        return GenericSummary(**data)
