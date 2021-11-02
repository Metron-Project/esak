"""
Events module.

This module provides the following classes:

- Event
- EventSchema
- EventsList
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load
from marshmallow.exceptions import ValidationError

from esak import exceptions, generic_summary, utils


class Events:
    """
    The Event object contains information for events.

    :param `**kwargs`: The keyword arguments is used for setting event data from Marvel.
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
    resource_uri = fields.Str(data_key="resourceURI")
    # urls
    modified = fields.DateTime()
    start = fields.Date(allow_none=True)
    end = fields.Date(allow_none=True)
    thumbnail = fields.Url()
    comics = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    stories = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    series = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    characters = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    creators = fields.Nested(generic_summary.GenericSummarySchema, many=True)
    next = fields.Nested(generic_summary.GenericSummarySchema, allow_none=True)
    previous = fields.Nested(generic_summary.GenericSummarySchema, allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"

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
                result = EventSchema().load(events_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

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
