"""
Creator Summary module.

This module provides the following classes:

- CreatorSummary
- CreatorSummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class CreatorSummary:
    def __init__(self, id=None, name=None, role=None, resource_uri=None, **kwargs):
        self.id = id
        self.name = name
        self.role = role
        self.resource_uri = resource_uri
        self.unknown = kwargs


class CreatorSummarySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    role = fields.Str()
    resourceURI = fields.Url(attribute="resource_uri")

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kwargs):
        return CreatorSummary(**data)
