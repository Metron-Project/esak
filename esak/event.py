"""
Events module.

This module provides the following classes:

- Event
- EventSchema
- EventsList
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, summary, utils


class Events:
    """
    The Event object contains information for events.

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting data from Marvel.

    Attributes
    ----------
    id: int
        The unique ID of the event resource.
    title: str
        The title of the event.
    description: str
        A description of the event.
    resource_uri: url
        The canonical URL identifier for this resource.
    modified: datetime
        The date the resource was most recently modified.
    start: date
        The date of publication of the first issue in this event.
    end: date
        The date of publication of the last issue in this event.
    thumbnail: url
        The representative image for this event.
    comics: list(Summary)
        A resource list containing the comics in this event.
    stories: list(Summary)
        A resource list containing the stories in this event.
    series: list(Summary)
        A resource list containing the series in this event.
    characters: list(Summary)
        A resource list containing the characters which appear in this event.
    creators: list(Summary)
        A resource list containing creators whose work appears in this event.
    next: list(Summary)
        A summary representation of the event which follows this event.
    previous: list(Summary)
        A summary representation of the event which preceded this event.
    """

    def __init__(self, **kwargs) -> None:
        """Intialize a new event."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class EventSchema(Schema):
    """Schema for the Event API."""

    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    resource_uri = fields.Url(data_key="resourceURI")
    # urls
    modified = fields.DateTime()
    start = fields.Date(allow_none=True)
    end = fields.Date(allow_none=True)
    thumbnail = fields.Url()
    comics = fields.Nested(summary.SummarySchema, many=True)
    stories = fields.Nested(summary.SummarySchema, many=True)
    series = fields.Nested(summary.SummarySchema, many=True)
    characters = fields.Nested(summary.SummarySchema, many=True)
    creators = fields.Nested(summary.SummarySchema, many=True)
    next = fields.Nested(summary.SummarySchema, allow_none=True)
    previous = fields.Nested(summary.SummarySchema, allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"

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

        resources = ["stories", "characters", "creators", "comics", "series"]
        for i in resources:
            if i in data:
                data[i] = data[i]["items"]

        if "thumbnail" in data:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        return data

    @post_load
    def make(self, data, **kargs):
        """
        Make the events object.

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        Event
            A Event object
        """
        return Events(**data)


class EventsList:
    """The EventsList object contains a list of `Events` objects."""

    def __init__(self, response):
        """Initialize a new EventsList."""
        self.events = []

        for events_dict in response["data"]["results"]:
            try:
                result = EventSchema().load(events_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error) from error

            self.events.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.events)

    def __len__(self):
        """Return the length of the object."""
        return len(self.events)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.events[index]
