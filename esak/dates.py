"""
Dates module.

This module provides the following classes:

- Dates
- DatesSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Dates:
    """
    The Dates object contains common dates.

    :param `on_sale`: The date the comic went on sale.
    :param `foc`: The final order cutoff date.
    :param `unlimited`: The date it was release on Marvel Unlimited.
    :param `**kwargs`: The keyword arguments used for setting any other date from Marvel.
    """

    def __init__(self, on_sale=None, foc=None, unlimited=None, **kwargs):
        """Intialize a new date."""
        self.on_sale = on_sale
        self.foc = foc
        self.unlimited = unlimited
        self.unknown = kwargs


class DatesSchema(Schema):
    """Schema for the Dates."""

    onsaleDate = fields.Date(attribute="on_sale")
    focDate = fields.Date(attribute="foc")
    unlimitedDate = fields.Date(attribute="unlimited")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE
        dateformat = "%Y-%m-%dT%H:%M:%S%z"

    @pre_load
    def process_input(self, data, **kwargs):
        """Clean up response data."""
        # Marvel comic 4373, and maybe others, returns a focDate of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        return {d["type"]: d["date"] for d in data if d["date"][0] != "-"}

    @post_load
    def make(self, data, **kwargs):
        """
        Make the dates object.

        :param data: Data from Marvel response.

        :returns: :class:`Dates` object
        :rtype: Dates
        """
        return Dates(**data)
