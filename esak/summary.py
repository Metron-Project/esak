"""
Summary module.

This module provides the following classes:

- Summary
- SummarySchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Summary:
    """
    The Summary object contains basic information.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting summary data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the summary resource.
    name: str
        The name of the summary.
    resource_uri: url
        The path to the individual summary resource.
    type: str
        The summary type.
    role: str
        The role of the summary in the parent entity.
    """

    def __init__(self, id=None, name=None, resource_uri=None, type=None, role=None, **kwargs):
        """Intialize a new Summary."""
        self.id = id
        self.name = name
        self.resource_uri = resource_uri
        self.type = type
        self.role = role
        self.unknown = kwargs


class SummarySchema(Schema):
    """Schema for the Summary."""

    id = fields.Int()
    name = fields.Str()
    resource_uri = fields.Url(data_key="resourceURI")
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
        Make the Summary object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Summary
            A Summary object
        """
        return Summary(**data)
