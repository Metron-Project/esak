"""
Prices module.

This module provides the following classes:

- Prices
- PricesSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Prices:
    """
    The Prices object contains price information.

    Parameters
    ----------
    print: decimal
        The price of print comic.
    digital: decimal
        The price of digital comic.
    **kwargs
        The keyword arguments used for setting any other price from Marvel.

    Attributes
    ----------
    print: decimal
        The price of print comic.
    digital: decimal
        The price of digital comic.
    """

    def __init__(self, print=None, digital=None, **kwargs):
        """Intialize a new price."""
        self.print = print
        self.digital = digital
        self.unknown = kwargs


class PriceSchemas(Schema):
    """Schema for the Prices."""

    print = fields.Decimal(places=2, data_key="printPrice")
    digital = fields.Decimal(places=2, data_key="digitalPurchasePrice")

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Clean up response data."""
        return {d["type"]: d["price"] for idx, d in enumerate(data, 0) if d["type"][idx]}

    @post_load
    def make(self, data, **kwargs):
        """
        Make the prices object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Prices
            A Prices object
        """
        return Prices(**data)
