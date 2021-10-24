"""
Events Summary module.

This module provides the following classes:

- EventsSummary
- EventsSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class EventSummary:
    """
    The EventSummary object contains basic information for events.

    :param `**kwargs`: The keyword arguments used for getting event data from Marvel.
    """

    def __init__(self, id=None, name=None, resource_uri=None, **kwargs):
        """Intialize a new EventSummary."""
        self.id = id
        self.name = name
        self.resource_uri = resource_uri
        self.unknown = kwargs


class EventSummarySchema(Schema):
    """Schema for the EventSummary."""

    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Event Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the EventSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`EventSummary` object
        :rtype: EventSummary
        """
        return EventSummary(**data)
