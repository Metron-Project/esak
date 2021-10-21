"""
CharactersList module.

This module provides the following classes:

- CharactersList
"""
import itertools

from marshmallow import ValidationError

from . import character, exceptions


class CharactersList:
    """The CharactersList object contains a list of `Character` objects."""

    def __init__(self, response):
        """Initialize a new CharactersList."""
        self.character = []

        schema = character.CharactersSchema()
        for character_dict in response["data"]["results"]:
            try:
                result = schema.load(character_dict)
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
