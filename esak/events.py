"""
Events module.

This module provides the following classes:

- Events
- EventsSchema
- EventsList
"""
import itertools

from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import character, comic_summary, creator, events_summary, exceptions, story_summary


class Events:
    """
    The Events object contains information for events.

    :param `**kwargs`: The keyword arguments is used for setting events data from Marvel.
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class EventsSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    resourceURI = fields.Str(attribute="resource_uri")
    # urls
    modified = fields.DateTime()
    start = fields.Date()
    end = fields.Date()
    thumbnail = fields.Url()
    comics = fields.Nested(comic_summary.ComicSummarySchema, many=True)
    stories = fields.Nested(story_summary.StorySummarySchema, many=True)
    # series
    characters = fields.Nested(character.CharacterSchema, many=True)
    creators = fields.Nested(creator.CreatorsSchema, many=True)
    next = fields.Nested(events_summary.EventSummarySchema)
    previous = fields.Nested(events_summary.EventSummarySchema)

    class Meta:
        unknown = INCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data = data["data"]["results"][0]

        if "stories" in data:
            data["stories"] = data["stories"]["items"]

        if "characters" in data:
            data["characters"] = data["characters"]["items"]

        if "creators" in data:
            data["creators"] = data["creators"]["items"]

        if "comics" in data:
            data["comics"] = data["comics"]["items"]

        if "thumbnail" in data:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        return data

    @post_load
    def make(self, data, **kargs):
        """
        Make the events object.

        :param data: Data from Marvel response.

        :returns: :class:`Events` object
        :rtype: Events
        """
        return Events(**data)


class EventsList:
    """The EventsList object contains a list of `Events` objects."""

    def __init__(self, response):
        """Initialize a new EventsList."""
        self.events = []

        for events_dict in response["data"]["results"]:
            try:
                result = EventsSchema().load(events_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.events.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.events)

    def __len__(self):
        """Return the length of the object."""
        return len(self.events)

    def __getitem__(self, index):
        """Return the object of a at index."""
        try:
            return next(itertools.islice(self.events, index, index + 1))
        except TypeError:
            return list(itertools.islice(self.events, index.start, index.stop, index.step))
