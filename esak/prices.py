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

    :param `print`: The price of print comic.
    :param `digital`: The price of digital comic.
    :param `**kwargs`: The keyword arguments used for setting any other price from Marvel.
    """

    def __init__(self, print=None, digital=None, **kwargs):
        """Intialize a new price."""
        self.print = print
        self.digital = digital
        self.unknown = kwargs


class PriceSchemas(Schema):
    """Schema for the Prices."""

    printPrice = fields.Decimal(places=2, attribute="print")
    digitalPurchasePrice = fields.Decimal(places=2, attribute="digital")

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

        :param data: Data from Marvel response.

        :returns: :class:`Prices` object
        :rtype: Prices
        """
        return Prices(**data)
