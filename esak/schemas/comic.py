"""The Comic module.

This module provides the following classes:

- Comic
"""

from __future__ import annotations

__all__ = ["Comic"]
from datetime import date, datetime
from decimal import Decimal

from pydantic import ConfigDict, Field, HttpUrl, field_validator

from esak.schemas import BaseModel
from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Dates(BaseModel):
    """The Dates object contains common dates.

    Attributes
    ----------
        on_sale: date | None
            Date the comic went on sale.
        foc: date | None
            The final order cutoff date.
        unlimited: date | None
            The date it was release on Marvel Unlimited.
        digital: date | None
            The date it was released digitally.
    """

    on_sale: date | None = Field(alias="onsaleDate", default=None)
    foc: date | None = Field(alias="focDate", default=None)
    unlimited: date | None = Field(alias="unlimitedDate", default=None)
    digital: date | None = Field(alias="digitalPurchaseDate", default=None)

    @field_validator("on_sale", "foc", "unlimited", "digital", mode="before")
    def datetime_to_date(cls, value: str | None) -> date | None:
        """Convert optional string to date.

        Parameters
        ----------
            value: str | None
                String value to parse as date

        Returns
        -------
            Parsed date or None
        """
        if value:
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z").date()
        return None


class Prices(BaseModel):
    """The Prices object contains price information.

    Attributes
    ----------
        print: Decimal | None
            The price of print comic.
        digital: Decimal | None
            The price of digital comic.
    """

    print: Decimal | None = Field(alias="printPrice", decimal_places=2, default=None)
    digital: Decimal | None = Field(
        alias="digitalPurchasePrice", decimal_places=2, default=None
    )


class TextObject(BaseModel):
    """The TextObject object contains basic information.

    Attributes
    ----------
        type: str
            The canonical type of the text object (e.g. solicit text, preview text, etc.).
        language: str
            The IETF language tag denoting the language the text object is written in.
        text: str
            The text.
    """

    type: str
    language: str
    text: str


class Comic(BaseResource):
    """The Comic object contains information for a comic.

    Attributes
    ----------
        digital_id: int
            The ID of the digital comic representation of this comic. Will be 0 if the comic is not available digitally.
        title: str
            The canonical title of the comic.
        issue_number: str
            The number of the issue in the series (will generally be 0 for collection formats).
        variant_description: str
            If the issue is a variant (e.g. an alternate cover, second printing, or director’s cut), a text description of the variant.
        description: str | None
            The preferred description of the comic.
        isbn: str | None
            The ISBN for the comic (generally only populated for collection formats).
        upc: str
            The UPC barcode number for the comic (generally only populated for periodical formats).
        diamond_code: str | None
            The Diamond code for the comic.
        ean: str
            The EAN barcode for the comic.
        issn: str
            The ISSN barcode for the comic.
        format: str
            The publication format of the comic e.g. comic, hardcover, trade paperback.
        page_count: int
            The number of story pages in the comic.
        text_objects: list[TextObject]
            A set of descriptive text blurbs for the comic.
        series: GenericItem
            A summary representation of the series to which this comic belongs.
        variants: list[GenericItem]
            A list of variant issues for this comic (includes the "original" issue if the current issue is a variant).
        collections: list[GenericItem]
            A list of collections which include this comic (will generally be empty if the comic's format is a collection).
        collected_issues: list[GenericItem]
            A list of issues collected in this comic (will generally be empty for periodical formats such as "comic" or "magazine").
        dates: Dates
            A list of key dates for this comic.
        prices: Prices
            A list of prices for this comic.
        images: list[HttpUrl]
            A list of promotional images associated with this comic.
        creators: list[GenericCreator]
            A resource list containing the creators associated with this comic.
        characters: list[GenericItem]
            A resource list containing the characters which appear in this comic.
        stories: list[GenericStory]
            A resource list containing the stories which appear in this comic.
        events: list[GenericItem]
            A resource list containing the events in which this comic appears.
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)

    digital_id: int
    title: str
    issue_number: str
    variant_description: str  # or Blank
    description: str | None = None
    isbn: str | None = None
    upc: str
    diamond_code: str | None = None
    ean: str  # or Blank
    issn: str  # or Blank
    format: str
    page_count: int
    text_objects: list[TextObject]
    series: GenericItem
    variants: list[GenericItem]
    collections: list[GenericItem]
    collected_issues: list[GenericItem]
    dates: Dates
    prices: Prices
    images: list[HttpUrl]
    creators: list[GenericCreator]
    characters: list[GenericItem]
    stories: list[GenericStory]
    events: list[GenericItem]

    @field_validator("diamond_code", "isbn", mode="before")
    def enforce_str(cls, value: str | int | None) -> str | None:
        """Enforce an int to be a str.

        Parameters
        ----------
            value: str | int | None
                Value to be converted

        Returns
        -------
            String value of input or None
        """
        if value:
            return str(value)
        return None

    @field_validator("dates", mode="before")
    def map_dates(cls, value: list[dict[str, str]]) -> dict[str, str]:
        """Convert list of Date objects to a dict that resembles a Dates object.

        Parameters
        ----------
            value: list[dict[str, str]]
                Dates object list

        Returns
        -------
            Dict mapping for a Dates object
        """
        return {x["type"]: x["date"] for x in value if x["date"][0] != "-"}

    @field_validator("prices", mode="before")
    def map_prices(cls, value: list[dict[str, str | Decimal]]) -> dict[str, Decimal]:
        """Convert list of Price objects to a dict that resembles a Prices object.

        Parameters
        ----------
            value: list[dict[str, str]]
                Prices object list

        Returns
        -------
            Dict mapping for a Prices object
        """
        return {x["type"]: x["price"] for x in value if x["price"]}

    @field_validator("images", mode="before")
    def map_images(cls, value: list[dict[str, str]]) -> list[str]:
        """Convert a list of url objects to a list or url strings by joining the path and extension.

        Parameters
        ----------
            value: list[dict[str, str]]
                List of url objects

        Returns
        -------
            List of url strings
        """
        return [f"{x['path']}.{x['extension']}" for x in value]

    @field_validator("creators", "characters", "stories", "events", mode="before")
    def map_generic_items(cls, value: dict) -> list[dict]:
        """Convert GenericItems to a list via the 'items' key.

        Parameters
        ----------
            value: dict
                Dict of subresource

        Returns
        -------
            List value of the 'items' key
        """
        return value["items"]
