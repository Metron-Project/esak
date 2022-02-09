"""
Stories module.

This module provides the following classes:

- Stories
- StoriesSchema
- StoriesList
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, summary, utils


class Stories:
    """
    The Stories object contains information for stories.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting stories data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the story resource.
    title: str
        The story title.
    descriptions: str
        A short description of the story.
    resource_uri: url
        The canonical URL identifier for this resource.
    type: str
        The story type e.g. interior story, cover, text story.
    modified: datetime
        The date the resource was most recently modified.
    thumbnail: url
        The representative image for this story.
    comics: list(Summary)
        A resource list containing comics in which this story takes place.
    series: list(Summary)
        A resource list containing series in which this story appears.
    events: list(Summary)
        A resource list of the events in which this story appears.
    characters: list(Summary)
        A resource list of characters which appear in this story.
    creators: list(Summary)
        A resource list of creators who worked on this story.
    original_issue: list(Summary)
        A summary representation of the issue in which this story was originally published.
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
    resource_uri = fields.Url(data_key="resourceURI")
    type = fields.Str()
    modified = fields.DateTime()
    thumbnail = fields.Url(allow_none=True)
    comics = fields.Nested(summary.SummarySchema, many=True)
    series = fields.Nested(summary.SummarySchema, many=True)
    events = fields.Nested(summary.SummarySchema, many=True)
    characters = fields.Nested(summary.SummarySchema, many=True)
    creators = fields.Nested(summary.SummarySchema, many=True)
    original_issue = fields.Nested(summary.SummarySchema, data_key="originalIssue")

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

        resources = ["series", "events", "creators", "characters", "comics"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]

        return data

    @post_load
    def make(self, data, **kargs):
        """
        Make the stories object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Stories
            A Stories object
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
                raise exceptions.ApiError(error) from error

            self.stories.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.stories)

    def __len__(self):
        """Return the length of the object."""
        return len(self.stories)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.stories[index]
