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

    Parameters
    ----------
    **kwargs
        The keyword arguments used for setting textobject data from Marvel.

    Attributes
    ----------
    type: str
        The canonical type of the text object (e.g. solicit text, preview text, etc.).
    language: str
        The IETF language tag denoting the language the text object is written in.
    text: str
        The text.
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

        Parameters
        ----------
        data
            Data from a Marvel API response.

        Returns
        -------
        TextObject
            A TextObject object
        """
        return TextObject(**data)
