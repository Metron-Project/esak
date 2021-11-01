"""
TextObject module.

This module provides the following classes:

- TextObject
- TextObjectSchema
"""
from marshmallow import Schema, fields, post_load


class TextObject:
    """
    The TextObject object contains basic information.

    :param `**kwargs`: The keyword arguments used for getting data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new TextObjects."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class TextObjectSchema(Schema):
    """Schema for the TextObject."""

    type = fields.Str()
    language = fields.Str()
    text = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        """
        Make the TextObject object.

        :param data: Data from Marvel response.

        :returns: :class:`TextObject` object
        :rtype: TextObject
        """
        return TextObject(**data)
