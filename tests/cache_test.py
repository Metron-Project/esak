"""Test Cache module.

This module contains tests for SqliteCache objects.
"""

import json

import pytest
import requests_mock

from esak import api
from esak.exceptions import CacheError
from esak.sqlite_cache import SqliteCache


class NoGet:
    """Test class mocking a Cache class without a get function."""

    def store(self, key: str, value: str) -> None:  # noqa: ARG002
        """Mock storing an entry in the cache."""
        return


class NoStore:
    """Test class mocking a Cache class without a store function."""

    def get(self, key: str) -> None:  # noqa: ARG002
        """Mock getting an entry from the cache."""
        return


def test_no_get(dummy_pubkey: str, dummy_privkey: str) -> None:
    """Test using a cache without a get function."""
    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=NoGet())

    with pytest.raises(CacheError):
        m.series(466)


def test_no_store(dummy_pubkey: str, dummy_privkey: str) -> None:
    """Test using a cache without a store function."""
    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=NoStore())

    with requests_mock.Mocker() as r:
        r.get("http://gateway.marvel.com:80/v1/public/series/466", text='{"response_code": 200}')

        with pytest.raises(CacheError):
            m.series(466)


def test_sql_store(dummy_pubkey: str, dummy_privkey: str) -> None:
    """Test that the cache is used with set."""
    fresh_cache = SqliteCache(":memory:")
    test_cache = SqliteCache("tests/testing_mock.sqlite")

    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=fresh_cache)
    url = "http://gateway.marvel.com:80/v1/public/series/466"

    assert fresh_cache.get(url) is None

    try:
        with requests_mock.Mocker() as r:
            r.get(url, text=json.dumps(test_cache.get(url)))
            m.series(466)

        assert fresh_cache.get(url) is not None
    except TypeError:
        print(
            "This test will fail after cache db deleted.\n"
            "It should pass if you now re-run the test suite "
            "without deleting the database."
        )
        raise AssertionError from None
