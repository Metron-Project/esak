"""
Test Events module.

This module contains tests for Event objects.
"""
import datetime

import pytest

from esak import exceptions


def test_known_event(talker):
    se = talker.event(336)
    assert se.title == "Secret Empire"
    assert se.start == datetime.date(2017, 4, 19)
    assert se.end == datetime.date(2017, 8, 9)
    assert se.resource_uri == "http://gateway.marvel.com/v1/public/events/336"
    assert se.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/6/f0/58e692d6f351b.jpg"

    assert len(se.stories) == 20
    assert se.stories[0].id == 109335
    assert se.stories[0].name == "cover from Deadpool (2012) #32"
    assert se.stories[0].type == "cover"

    assert len(se.characters) == 20
    assert se.characters[0].id == 1011227
    assert se.characters[0].name == "Amadeus Cho"
    assert (
        se.characters[0].resource_uri
        == "http://gateway.marvel.com/v1/public/characters/1011227"
    )

    assert len(se.creators) == 20
    assert se.creators[0].id == 11482
    assert se.creators[0].name == "Jesus Aburtov"
    assert se.creators[0].role == "colorist (cover)"

    assert se.next.id == 322
    assert se.next.name == "Avengers NOW!"
    assert se.previous.id == 332
    assert se.previous.name == "Dead No More: The Clone Conspiracy"

    assert len(se.comics) == 20
    assert se.comics[0].id == 63223
    assert se.comics[0].name == "All-New Guardians of the Galaxy Annual (2017) #1"
    assert se.comics[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/63223"

    assert len(se.series) == 20
    assert se.series[11].id == 25356
    assert se.series[11].name == "Secret Empire Omega (2017)"
    assert se.series[11].resource_uri == "http://gateway.marvel.com/v1/public/series/25356"


def test_bad_event(talker):
    with pytest.raises(exceptions.ApiError):
        talker.event(-1)


def test_events_list(talker):
    events_lst = talker.events_list(
        {
            "orderBy": "modified",
        }
    )

    stories_iter = iter(events_lst)
    assert (next(stories_iter).id) == 296
    assert (next(stories_iter).id) == 302
    assert (next(stories_iter).id) == 233
    assert len(events_lst) == 20
