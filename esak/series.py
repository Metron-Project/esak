"""
Series module.

This module provides the following classes:

- Series
- SeriesSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, summary, utils


class Series:
    """
    The Series object contains information for a series.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the series resource.
    title: str
        The canonical title of the series.
    description: str
        A description of the series.
    resource_uri: url
        The canonical URL identifier for this resource.
    start_year: int
        The first year of publication for the series.
    end_year: int
        The last year of publication for the series (conventionally, 2099 for ongoing series).
    rating: str
        The age-appropriateness rating for the series.
    modified: datetime
        The date the resource was most recently modified.
    thumbnail: url
        The representative image for this series.
    comics: list(Summary)
        A resource list containing comics in this series.
    stories: list(Summary)
        A resource list containing stories which occur in comics in this series.
    events: list(Summary)
        A resource list containing events which take place in comics in this series.
    characters: list(Summary)
        A resource list containing characters which appear in comics in this series.
    creators: list(Summary)
        A resource list of creators whose work appears in comics in this series.
    next: list(Summary)
        A summary representation of the series which follows this series.
    previous: list(Summary)
        A summary representation of the series which preceded this series.
    """

    def __init__(self, **kwargs):
        """Intialize a new series."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class SeriesSchema(Schema):
    """Schema for the Comic API."""

    id = fields.Int()
    title = fields.Str()
    description = fields.Str(allow_none=True)
    resource_uri = fields.Url(data_key="resourceURI")
    # urls
    start_year = fields.Int(data_key="startYear", allow_none=True)
    end_year = fields.Int(data_key="endYear", allow_none=True)
    rating = fields.Str(allow_none=True)
    modified = fields.DateTime()
    thumbnail = fields.URL(allow_none=True)
    comics = fields.Nested(summary.SummarySchema, many=True)
    stories = fields.Nested(summary.SummarySchema, many=True)
    events = fields.Nested(summary.SummarySchema, many=True)
    characters = fields.Nested(summary.SummarySchema, many=True)
    creators = fields.Nested(summary.SummarySchema, many=True)
    next = fields.Nested(summary.SummarySchema, allow_none=True)
    previous = fields.Nested(summary.SummarySchema, allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

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

        # Marvel series 6664, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if data.get("modified", " ")[0] == "-":
            del data["modified"]

        # derive ID
        data["id"] = data["resourceURI"].split("/")[-1]

        if "thumbnail" in data and data["thumbnail"] is not None:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
        else:
            data["thumbnail"] = None

        resources = ["comics", "stories", "events", "characters", "creators"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Series object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Series
            A Series object
        """
        return Series(**data)


class SeriesList:
    """The SeriesList object contains a list of `Series` objects."""

    def __init__(self, response):
        """Initialize a new SeriesList."""
        self.series = []

        for series_dict in response["data"]["results"]:
            try:
                result = SeriesSchema().load(series_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error

            self.series.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.series)

    def __len__(self):
        """Return the length of the object."""
        return len(self.series)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.series[index]
