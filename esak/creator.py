"""
Creator module.

This module provides the following classes:

- Creator
- CreatorSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, summary, utils


class Creator:
    """
    The Creator object contains information for creators.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting character data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the creator resource.
    first_name: str
        The first name of the creator.
    middle_name: str
        The middle name of the creator.
    last_name: str
        The last name of the creator.
    suffix: str
        The suffix or honorific for the creator.
    full_name: str
        The full name of the creator (a space-separated concatenation of the
        above four fields).
    modified: datetime
        The date the resource was most recently modified.
    resource_uri: url
        The canonical URL identifier for this resource.
    thumbnail: url
        The representative image for this creator.
    series: list(Summary)
        A resource list containing the series which feature work by this creator.
    stories: list(Summary)
        A resource list containing the stories which feature work by this creator.
    events: list(Summary)
        A resource list containing the events which feature work by this creator.
    comics: list(Summary)
        A resource list containing the comics which feature work by this creator.
    """

    def __init__(self, **kwargs):
        """Intialize a new Creator."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorsSchema(Schema):
    """Schema for the Creator API."""

    id = fields.Int()
    first_name = fields.Str(data_key="firstName")
    middle_name = fields.Str(data_key="middleName")
    last_name = fields.Str(data_key="lastName")
    suffix = fields.Str()
    full_name = fields.Str(data_key="fullName")
    modified = fields.DateTime()
    resource_uri = fields.Str(data_key="resourceURI")
    # urls
    thumbnail = fields.Url()
    series = fields.Nested(summary.SummarySchema, many=True)
    stories = fields.Nested(summary.SummarySchema, many=True)
    events = fields.Nested(summary.SummarySchema, many=True)
    comics = fields.Nested(summary.SummarySchema, many=True)

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

        if "thumbnail" in data:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        data["id"] = data["resourceURI"].split("/")[-1]

        resources = ["events", "series", "stories", "comics"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Creator object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Creator
            A Creator object
        """
        return Creator(**data)


class CreatorsList:
    """The CreatorsList object contains a list of `Creator` objects."""

    def __init__(self, response):
        """Initialize a new CreatorsList."""
        self.creator = []

        for series_dict in response["data"]["results"]:
            try:
                result = CreatorsSchema().load(series_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error

            self.creator.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.creator)

    def __len__(self):
        """Return the length of the object."""
        return len(self.creator)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.creator[index]
