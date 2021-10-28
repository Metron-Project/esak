"""
Creator module.

This module provides the following classes:

- Creator
- CreatorSchema
"""
import itertools

from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, generic_summary


class Creator:
    """
    The Creator object contains information for creators.

    :param `**kwargs`: The keyword arguments is used for setting creator data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new Creator."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorsSchema(Schema):
    """Schema for the Creator API."""

    id = fields.Int()
    firstName = fields.Str(attribute="first_name")
    middleName = fields.Str(attribute="middle_name")
    lastName = fields.Str(attribute="last_name")
    suffix = fields.Str()
    fullName = fields.Str(attribute="full_name")
    modified = fields.DateTime()
    resourceURI = fields.Str(attribute="resource_uri")
    # urls
    thumbnail = fields.Url()
    series = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    stories = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    events = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    comics = fields.Nested(generic_summary.GenericSummarySchema, many=True)

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

        if "thumbnail" in data:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "series" in data:
            data["series"] = data["series"]["items"]

        if "stories" in data:
            data["stories"] = data["stories"]["items"]

        if "comics" in data:
            data["comics"] = data["comics"]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the Creator object.

        :param data: Data from Marvel response.

        :returns: :class:`Creator` object
        :rtype: Creator
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
                raise exceptions.ApiError(error)

            self.creator.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.creator)

    def __len__(self):
        """Return the length of the object."""
        return len(self.creator)

    def __getitem__(self, index):
        """Return the object of a at index."""
        try:
            return next(itertools.islice(self.creator, index, index + 1))
        except TypeError:
            return list(itertools.islice(self.creator, index.start, index.stop, index.step))
