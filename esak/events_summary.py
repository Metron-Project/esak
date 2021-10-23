"""
Events Summary module.

This module provides the following classes:

- EventsSummary
- EventsSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class EventSummary:
    def __init__(self, id=None, name=None, resource_uri=None, **kwargs):
        self.id = id
        self.name = name
        self.resource_uri = resource_uri
        self.unknown = kwargs


class EventSummarySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return EventSummary(**data)
