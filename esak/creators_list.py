"""
CreatorsList module.

This module provides the following classes:

- CreatorsList
"""
import itertools

from marshmallow import ValidationError

from . import creator, exceptions


class CreatorsList:
    """The CreatorsList object contains a list of `Creator` objects."""

    def __init__(self, response):
        """Initialize a new CreatorsList."""
        self.creator = []

        schema = creator.CreatorsSchema()
        for series_dict in response["data"]["results"]:
            try:
                result = schema.load(series_dict)
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
