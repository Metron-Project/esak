"""
Comic module.

This module provides the following classes:

- Comic
- ComicSchema
- ComicsList
"""
from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import dates, exceptions, prices, series, summary, text_object, urls, utils


class Comic:
    """
    The Comic object contains information for a comic.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the comic resource.
    digital_id: int
        The ID of the digital comic representation of this comic. Will be 0 if the comic is not
        available digitally.
    title: str
        The canonical title of the comic.
    issue_number: int
        The number of the issue in the series (will generally be 0 for collection formats).
    variant_description: str
        If the issue is a variant (e.g. an alternate cover, second printing,
        or director’s cut), a text description of the variant.
    description: str, optional
        The preferred description of the comic.
    modified: datetime
        The date the resource was most recently modified.
    isbn: str
        The ISBN for the comic (generally only populated for collection formats).
    upc: str
        The UPC barcode number for the comic (generally only populated for periodical formats).
    diamond_code: str
        The Diamond code for the comic.
    ean: str
        The EAN barcode for the comic.
    issn: str
        The ISSN barcode for the comic.
    format: str
        The publication format of the comic e.g. comic, hardcover, trade paperback.
    page_count: int
        The number of story pages in the comic.
    text_objects: list(TextObject)
        A set of descriptive text blurbs for the comic.
    resource_uri: url
        The canonical URL identifier for this resource.
    urls: list(Urls)
        A set of public web site URLs for the resource.
    series: list(Series)
        A summary representation of the series to which this comic belongs.
    variants: list(Summary)
        A list of variant issues for this comic (includes the "original" issue if the current
        issue is a variant).
    collections: list(Summary)
        A list of collections which include this comic (will generally be empty if the comic's
        format is a collection).
    collected_issues: list(Summary)
        A list of issues collected in this comic (will generally be empty for periodical
        formats such as "comic" or "magazine").
    dates: list(Dates)
        A list of key dates for this comic.
    prices: list(Price)
        A list of prices for this comic.
    thumbnail: url
        The representative image for this comic.
    images: list(url)
        A list of promotional images associated with this comic.
    creators: list(Summary)
        A resource list containing the creators associated with this comic.
    characters: list(Summary)
        A resource list containing the characters which appear in this comic.
    stories: list(Summary)
        A resource list containing the stories which appear in this comic.
    events: list(Summary)
        A resource list containing the events in which this comic appears.
    """

    def __init__(self, **kwargs):
        """Intialize a new comic."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSchema(Schema):
    """
    Schema for the Comic API.

    .. versionchanged:: 1.3.0

        - Added ``thumbnail`` and ``text_objects`` fields.
        - Unknowns fields will now be **excluded**.
    """

    id = fields.Int()
    digital_id = fields.Int(data_key="digitalId")
    title = fields.Str()
    issue_number = fields.Int(data_key="issueNumber")
    variant_description = fields.Str(data_key="variantDescription")
    description = fields.Str(allow_none=True)
    modified = fields.DateTime()
    isbn = fields.Str()
    upc = fields.Str()
    diamond_code = fields.Str(data_key="diamondCode")
    ean = fields.Str()
    issn = fields.Str()
    format = fields.Str()
    page_count = fields.Int(data_key="pageCount")
    text_objects = fields.Nested(
        text_object.TextObjectSchema, data_key="textObjects", many=True
    )
    resource_uri = fields.Str(data_key="resourceURI")
    urls = fields.Nested(urls.UrlsSchema)
    series = fields.Nested(series.SeriesSchema)
    variants = fields.Nested(summary.SummarySchema, many=True)
    collections = fields.Nested(summary.SummarySchema, many=True)
    collected_issues = fields.Nested(
        summary.SummarySchema, data_key="collectedIssues", many=True
    )
    dates = fields.Nested(dates.DatesSchema)
    prices = fields.Nested(prices.PriceSchemas, allow_none=True)
    thumbnail = fields.Url()
    images = fields.List(fields.Url)
    creators = fields.Nested(summary.SummarySchema, many=True)
    characters = fields.Nested(summary.SummarySchema, many=True)
    stories = fields.Nested(summary.SummarySchema, many=True)
    events = fields.Nested(summary.SummarySchema, many=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """
        Clean the data from Marvel.

        Parameters
        ----------
        data
            Data from a Marvel api response.

        Returns
        -------
        dict
            Marvel response.
        """
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data = data["data"]["results"][0]

        data = utils.check_mod_date(data)

        resources = ["stories", "events", "creators", "characters"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        resources = ["isbn", "diamondCode"]
        for i in resources:
            if i in data:
                data[i] = str(data[i])

        if "images" in data:
            data["images"] = [f"{img['path']}.{img['extension']}" for img in data["images"]]

        if "thumbnail" in data and data["thumbnail"] is not None:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
        else:
            data["thumbnail"] = None

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Comic object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Comic
            A Comic object
        """
        return Comic(**data)


class ComicsList:
    """The ComicsList object contains a list of `Comic` objects."""

    def __init__(self, response):
        """Initialize a new ComicList."""
        self.comics = []

        for comic_dict in response["data"]["results"]:
            try:
                result = ComicSchema().load(comic_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error

            self.comics.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.comics)

    def __len__(self):
        """Return the length of the object."""
        return len(self.comics)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.comics[index]
