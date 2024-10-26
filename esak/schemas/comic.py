"""The Comic module.

This module provides the following classes:

- Comic
"""

__all__ = ["Comic"]
from datetime import date, datetime
from decimal import Decimal

from pydantic import ConfigDict, Field, HttpUrl, field_validator

from esak.schemas import BaseModel
from esak.schemas.base import BaseResource
from esak.schemas.generic import GenericCreator, GenericItem, GenericStory


class Dates(BaseModel):
    """The Dates object contains common dates.

    Attributes:
        on_sale: Date the comic went on sale.
        foc: The final order cutoff date.
        unlimited: The date it was release on Marvel Unlimited.
        digital: The date it was released digitally.
    """

    on_sale: date | None = Field(alias="onsaleDate", default=None)
    foc: date | None = Field(alias="focDate", default=None)
    unlimited: date | None = Field(alias="unlimitedDate", default=None)
    digital: date | None = Field(alias="digitalPurchaseDate", default=None)

    @field_validator("on_sale", "foc", "unlimited", "digital", mode="before")
    def datetime_to_date(cls, value: str | None) -> date | None:
        """Convert optional string to date.

        Args:
            value: String value to parse as date

        Returns:
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

    Attributes:
        print: The price of print comic.
        digital: The price of digital comic.
    """

    print: Decimal | None = Field(alias="printPrice", decimal_places=2, default=None)
    digital: Decimal | None = Field(alias="digitalPurchasePrice", decimal_places=2, default=None)


class TextObject(BaseModel):
    """The TextObject object contains basic information.

    Attributes:
        type: The canonical type of the text object (e.g. solicit text, preview text, etc.).
        language: The IETF language tag denoting the language the text object is written in.
        text: The text.
    """

    type: str
    language: str
    text: str


class Comic(BaseResource):
    """The Comic object contains information for a comic.

    Attributes:
        digital_id: The ID of the digital comic representation of this comic.
            Will be 0 if the comic is not available digitally.
        title: The canonical title of the comic.
        issue_number: The number of the issue in the series.
            Will generally be 0 for collection formats.
        variant_description: If the issue is a variant (e.g. an alternate cover,
            second printing, or director's cut), a text description of the variant.
        description: The preferred description of the comic.
        isbn: The ISBN for the comic (generally only populated for collection formats).
        upc: The UPC barcode number for the comic (generally only populated for periodical formats).
        diamond_code: The Diamond code for the comic.
        ean: The EAN barcode for the comic.
        issn: The ISSN barcode for the comic.
        format: The publication format of the comic e.g. comic, hardcover, trade paperback.
        page_count: The number of story pages in the comic.
        text_objects: A set of descriptive text blurbs for the comic.
        series: A summary representation of the series to which this comic belongs.
        variants: A list of variant issues for this comic (includes the "original"
            issue if the current issue is a variant).
        collections: A list of collections which include this comic (will generally
            be empty if the comic's format is a collection).
        collected_issues: A list of issues collected in this comic (will generally
            be empty for periodical formats such as "comic" or "magazine").
        dates: A list of key dates for this comic.
        prices: A list of prices for this comic.
        images: A list of promotional images associated with this comic.
        creators: A resource list containing the creators associated with this comic.
        characters: A resource list containing the characters which appear in this comic.
        stories: A resource list containing the stories which appear in this comic.
        events: A resource list containing the events in which this comic appears.
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

        Args:
            value: Value to be converted

        Returns:
            String value of input or None
        """
        return str(value) if value else None

    @field_validator("dates", mode="before")
    def map_dates(cls, value: list[dict[str, str]]) -> dict[str, str]:
        """Convert list of Date objects to a dict that resembles a Dates object.

        Args:
            value: Dates object list

        Returns:
            Dict mapping for a Dates object
        """
        return {x["type"]: x["date"] for x in value if x["date"][0] != "-"}

    @field_validator("prices", mode="before")
    def map_prices(cls, value: list[dict[str, str | Decimal]]) -> dict[str, Decimal]:
        """Convert list of Price objects to a dict that resembles a Prices object.

        Args:
            value: Prices object list

        Returns:
            Dict mapping for a Prices object
        """
        return {x["type"]: x["price"] for x in value if x["price"]}

    @field_validator("images", mode="before")
    def map_images(cls, value: list[dict[str, str]]) -> list[str]:
        """Convert a list of url objects to a list or url strings by joining the path and extension.

        Args:
            value: List of url objects

        Returns:
            List of url strings
        """
        return [f"{x['path']}.{x['extension']}" for x in value]

    @field_validator("creators", "characters", "stories", "events", mode="before")
    def map_generic_items(cls, value: dict) -> list[dict]:
        """Convert GenericItems to a list via the 'items' key.

        Args:
            value: Dict of subresource

        Returns:
            List value of the 'items' key
        """
        return value["items"]
