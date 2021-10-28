"""
Character module.

This module provides the following classes:

- Character
- CharacterSchema
"""
import itertools

from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, generic_summary, urls


class Character:
    """
    The Character object contains information for characters.

    :param `**kwargs`: The keyword arguments is used for setting character data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new Character."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CharacterSchema(Schema):
    """Schema for the Character API."""

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    modified = fields.DateTime()
    resourceURI = fields.Str(attribute="resource_uri")
    urls = fields.Nested(urls.UrlsSchema)
    thumbnail = fields.Url()
    comics = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    stories = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    events = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    series = fields.Nested(generic_summary.GenericSummarySchema, many=True)

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
        Make the character object.

        :param data: Data from Marvel response.

        :returns: :class:`Character` object
        :rtype: Character
        """
        return Character(**data)


class CharactersList:
    """The CharactersList object contains a list of `Character` objects."""

    def __init__(self, response):
        """Initialize a new CharactersList."""
        self.character = []

        for character_dict in response["data"]["results"]:
            try:
                result = CharacterSchema().load(character_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.character.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.character)

    def __len__(self):
        """Return the length of the object."""
        return len(self.character)

    def __getitem__(self, index):
        """Return the object of a at index."""
        try:
            return next(itertools.islice(self.character, index, index + 1))
        except TypeError:
            return list(itertools.islice(self.character, index.start, index.stop, index.step))
