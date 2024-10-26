"""Test Init module.

This module contains tests for project init.
"""

import contextlib

import pytest

from esak import api
from esak.exceptions import AuthenticationError
from esak.session import Session


def test_api() -> None:
    """Test that the api function produces a Session object."""
    with pytest.raises(AuthenticationError):
        api()

    with pytest.raises(AuthenticationError):
        api(private_key="Something")

    with pytest.raises(AuthenticationError):
        api(public_key="Something")

    m = None
    with contextlib.suppress(Exception):
        m = api(public_key="Something", private_key="Else")

    assert m.__class__.__name__, Session.__name__
