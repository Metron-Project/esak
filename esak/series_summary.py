"""
Series Summary module.

This module provides the following classes:

- SeriesSummary
- SeriesSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class SeriesSummary:
    """
    The SeriesSummary object contains basic information for series.

    :param `**kwargs`: The keyword arguments used for getting series data from Marvel.
    """

    def __init__(self, id=None, name=None, resource_uri=None, **kwargs):
        """Intialize a new SeriesSummary."""
        self.id = id
        self.name = name
        self.resource_uri = resource_uri
        self.unknown = kwargs


class SeriesSummarySchema(Schema):
    """Schema for the SeriesSummary."""

    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Series Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the SeriesSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`SeriesSummary` object
        :rtype: SeriesSummary
        """
        return SeriesSummary(**data)
