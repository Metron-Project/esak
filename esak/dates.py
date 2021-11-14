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

    Parameters
    ----------
    on_sale: date
        The date the comic went on sale.
    foc: date
        The final order cutoff date.
    unlimited: date
        The date it was release on Marvel Unlimited.
    **kwargs
        The keyword arguments used for setting any other date from Marvel.

    Attributes
    ----------
    on_sale: date
        The date the comic went on sale.
    foc: date
        The final order cutoff date.
    unlimited: date
        The date it was release on Marvel Unlimited.
    """

    def __init__(self, on_sale=None, foc=None, unlimited=None, **kwargs):
        """Intialize a new date."""
        self.on_sale = on_sale
        self.foc = foc
        self.unlimited = unlimited
        self.unknown = kwargs


class DatesSchema(Schema):
    """Schema for the Dates."""

    on_sale = fields.Date(data_key="onsaleDate")
    foc = fields.Date(data_key="focDate")
    unlimited = fields.Date(data_key="unlimitedDate")

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

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Dates
            A Date object
        """
        return Dates(**data)
