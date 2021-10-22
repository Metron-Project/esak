"""
Comic Summary module.

This module provides the following classes:

- ComicSummary
- ComicSummarySchema
"""

from marshmallow import Schema, fields, post_load, pre_load


class ComicSummary:
    """
    The ComicSummary object contains information for Comics.

    :param `**kwargs`: The keyword arguments used for setting comic summary data from Marvel.
    """

    def __init__(self, **kwargs) -> None:
        """Intialize a new ComicSummary."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSummarySchema(Schema):
    """Schema for the ComicSummary."""

    id = fields.Int()
    name = fields.Str()
    resourceURI = fields.Url(attribute="resource_uri")

    @pre_load
    def process_input(self, data, **kwargs):
        """Extract the Comic Summary id."""
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the ComicSummary object.

        :param data: Data from Marvel response.

        :returns: :class:`ComicSummary` object
        :rtype: ComicSummary
        """
        return ComicSummary(**data)
