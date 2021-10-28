"""
Comic module.

This module provides the following classes:

- Comic
- ComicSchema
- ComicsList
"""
import itertools

from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import dates, exceptions, generic_summary, prices, series, urls


class Comic:
    """
    The Comic object contains information for a comic.

    :param `**kwargs`: The keyword arguments is used for setting comic data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new comic."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSchema(Schema):
    """Schema for the Comic API."""

    id = fields.Int()
    digitalId = fields.Int(attribute="digital_id")
    title = fields.Str()
    issueNumber = fields.Int(attribute="issue_number")
    variantDescription = fields.Str(attribute="variant_description")
    description = fields.Str(allow_none=True)
    modified = fields.DateTime()
    isbn = fields.Str()
    upc = fields.Str()
    diamondCode = fields.Str(attribute="diamond_code")
    ean = fields.Str()
    issn = fields.Str()
    format = fields.Str()
    pageCount = fields.Int(attribute="page_count")
    # textObjects
    resourceURI = fields.Url(attribute="resource_uri")
    urls = fields.Nested(urls.UrlsSchema)
    series = fields.Nested(series.SeriesSchema)
    variants = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    collections = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    collectedIssues = fields.Nested(
        generic_summary.GenericSummarySchema, attribute="collected_issues", many=True
    )
    dates = fields.Nested(dates.DatesSchema)
    prices = fields.Nested(prices.PriceSchemas, allow_none=True)
    # thumbnail
    images = fields.List(fields.Url)
    creators = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    characters = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    stories = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    events = fields.Nested(generic_summary.GenericSummarySchema, many=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        """
        Clean the data from Marvel.

        :param data: Data from Marvel response.

        :returns: Marvel Response
        :rtype: dict
        """
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data = data["data"]["results"][0]

        # Marvel comic 1768, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if data.get("modified", " ")[0] == "-":
            del data["modified"]

        if "stories" in data:
            data["stories"] = data["stories"]["items"]

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "creators" in data:
            data["creators"] = data["creators"]["items"]

        if "characters" in data:
            data["characters"] = data["characters"]["items"]

        if "images" in data:
            data["images"] = [f"{img['path']}.{img['extension']}" for img in data["images"]]

        if "isbn" in data:
            data["isbn"] = str(data["isbn"])

        if "diamondCode" in data:
            data["diamondCode"] = str(data["diamondCode"])

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Comic object.

        :param data: Data from Marvel response.

        :returns: :class:`Comic` object
        :rtype: Comic
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
                raise exceptions.ApiError(error)

            self.comics.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.comics)

    def __len__(self):
        """Return the length of the object."""
        return len(self.comics)

    def __getitem__(self, index):
        """Return the object of a at index."""
        try:
            return next(itertools.islice(self.comics, index, index + 1))
        except TypeError:
            return list(itertools.islice(self.comics, index.start, index.stop, index.step))
