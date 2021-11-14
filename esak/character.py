"""
Character module.

This module provides the following classes:

- Character
- CharacterSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, summary, urls, utils


class Character:
    """
    The Character object contains information for characters.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting character data from Marvel.

    Attributes
    ----------
    id: int
        The Marvel id for the character.
    name: str
        The character name.
    description: str
        The character description.
    modified: datetime
        The date and time the character data was modified.
    resource_uri: str
        The url for the character.
    urls: list(Urls)
        A list of urls for the character.
    thumbnail: str
        The url for the character thumbnail image.
    comics: list(Comic)
        A list of comics the character appeared in.
    stories: list(Summary)
        A list of story summaries for the character.
    events: list(Summary)
        A list of event summaries for the character.
    series: list(Summary)
        A list of series summaries for the character.
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
    resource_uri = fields.Url(data_key="resourceURI")
    urls = fields.Nested(urls.UrlsSchema)
    thumbnail = fields.Url()
    comics = fields.Nested(summary.SummarySchema, many=True)
    stories = fields.Nested(summary.SummarySchema, many=True)
    events = fields.Nested(summary.SummarySchema, many=True)
    series = fields.Nested(summary.SummarySchema, many=True)

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

        if "thumbnail" in data and data["thumbnail"] is not None:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
        else:
            data["thumbnail"] = None

        resources = ["events", "series", "stories", "comics"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the character object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Character
            A Character object
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

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.character[index]
