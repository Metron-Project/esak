"""
Test Init module.
This module contains tests for project init.
"""

import pytest

from esak import api
from esak.exceptions import AuthenticationError
from esak.session import Session


def test_api():
    with pytest.raises(AuthenticationError):
        api()

    with pytest.raises(AuthenticationError):
        api(private_key="Something")

    with pytest.raises(AuthenticationError):
        api(public_key="Something")

    m = None
    try:
        m = api(public_key="Something", private_key="Else")
    except Exception as exc:
        print(f"mokkari.api() raised {exc} unexpectedly!")

    assert m.__class__.__name__, Session.__name__
