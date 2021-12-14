"""
Urls module.

This module provides the following classes:

- Urls
- UrlsSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Urls:
    """
    The Urls object contains commonly used urls.

    Parameters
    ----------
    digital_purchase_date
        The url for the digital_purchase_date
    foc_date
        The url for the final order cutoff date.
    onsale_date
        The url for the on sale date.
    unlimited_date
        The url for the Marvel Unlimited date.
    wiki
        The url for the wiki entry.
    detail
        The url for detail information.
    **kwargs
        The keyword arguments used for setting any other url from Marvel.

    Attributes
    ----------
    digital_purchase_date: Url
        The url for the digital_purchase_date
    foc_date: Url
        The url for the final order cutoff date.
    onsale_date: Url
        The url for the on sale date.
    unlimited_date: Url
        The url for the Marvel Unlimited date.
    wiki: Url
        The url for the wiki entry.
    detail: Url
        The url for detail information.
    """

    def __init__(
        self,
        digital_purchase_date=None,
        foc_date=None,
        onsale_date=None,
        unlimited_date=None,
        wiki=None,
        detail=None,
        **kwargs,
    ):
        """Intialize a new url."""
        self.digital_purchase_date = digital_purchase_date
        self.foc_date = foc_date
        self.onsale_date = onsale_date
        self.unlimited_date = unlimited_date
        self.wiki = wiki
        self.detail = detail
        self.unknown = kwargs


class UrlsSchema(Schema):
    """Schema for the Urls."""

    digital_purchase_date = fields.Url(data_key="digitalPurchaseDate")
    foc_date = fields.Url(data_key="focDate")
    onsale_date = fields.Url(data_key="onsaleDate")
    unlimited_date = fields.Url(data_key="unlimitedDate")
    # Should these go into a separate class like CharacterUrls?
    # For now let's put them here, but it may be something to consider to split them.
    wiki = fields.Url()
    detail = fields.Url()

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """Clean up response data."""
        return {d["type"]: d["url"] for d in data}

    @post_load
    def make(self, data, **kwargs):
        """
        Make the urls object.

        Parameters
        ----------
        data
            Data from a Marvel api response.

        Returns
        -------
        Urls
            A Urls object.
        """
        return Urls(**data)
