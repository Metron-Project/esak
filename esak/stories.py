"""
Stories module.

This module provides the following classes:

- Stories
- StoriesSchema
- StoriesList
"""
import itertools

from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, generic_summary


class Stories:
    """
    The Stories object contains information for stories.

    :param `**kwargs`: The keyword arguments is used for setting stories data from Marvel.
    """

    def __init__(self, **kwargs) -> None:
        """Intialize a new story."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoriesSchema(Schema):
    """Schema for the Stories API."""

    id = fields.Int()
    title = fields.Str()
    descriptions = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")
    type = fields.Str()
    modified = fields.DateTime()
    thumbnail = fields.Url(allow_none=True)
    comics = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    series = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    events = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    characters = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    creators = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    originalIssue = fields.Nested(
        generic_summary.GenericSummarySchema, attribute="original_issue"
    )

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

        if "thumbnail" in data and data["thumbnail"] is not None:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
        else:
            data["thumbnail"] = None

        if "series" in data:
            data["series"] = data["series"]["items"]

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "creators" in data:
            data["creators"] = data["creators"]["items"]

        if "characters" in data:
            data["characters"] = data["characters"]["items"]

        if "comics" in data:
            data["comics"] = data["comics"]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kargs):
        """
        Make the stories object.

        :param data: Data from Marvel response.

        :returns: :class:`Stories` object
        :rtype: Stories
        """
        return Stories(**data)


class StoriesList:
    """The StoriesList object contains a list of `Stories` objects."""

    def __init__(self, response):
        """Initialize a new StoriesList."""
        self.stories = []

        for stories_dict in response["data"]["results"]:
            try:
                result = StoriesSchema().load(stories_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.stories.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.stories)

    def __len__(self):
        """Return the length of the object."""
        return len(self.stories)

    def __getitem__(self, index):
        """Return the object of a at index."""
        try:
            return next(itertools.islice(self.stories, index, index + 1))
        except TypeError:
            return list(itertools.islice(self.stories, index.start, index.stop, index.step))
