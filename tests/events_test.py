"""
Test Events module.

This module contains tests for Event objects.
"""
import datetime
from decimal import Decimal

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
    assert events_lst[1].id == 302


def test_event_characters(talker):
    se = talker.event_characters(336)
    assert len(se) == 20
    ben = se[6]
    assert ben.id == 1010782
    assert ben.name == "Ben Urich"
    assert ben.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/5/90/4c00373d10e5e.jpg"
    assert len(ben.comics) == 20
    assert len(ben.events) == 4
    assert len(ben.series) == 20
    assert len(ben.stories) == 20


def test_event_comics(talker):
    se = talker.event_comics(336)
    assert len(se) == 20
    sm = se[11]
    assert sm.id == 60539
    assert sm.issue_number == 31
    assert sm.page_count == 32
    assert sm.upc == "75960608297103111"
    assert sm.title == "The Amazing Spider-Man (2017) #31"
    assert sm.prices.digital == Decimal("3.99")
    assert sm.prices.print == Decimal("3.99")
    assert sm.series.id == 20432
    assert sm.series.name == "The Amazing Spider-Man (2017 - 2018)"
    assert len(sm.characters) == 4
    assert len(sm.creators) == 7
    assert len(sm.events) == 1
    assert len(sm.stories) == 2
    solit = sm.text_objects[0]
    assert solit.language == "en-us"
    assert solit.type == "issue_solicit_text"
    assert (
        solit.text == "SECRET EMPIRE TIE-IN! On orders from Captain America, "
        "the Superior Octopus is taking the fight to Parker Industries. "
        "Peter must use the full force of his company to stop Ock and Hydra, "
        "but WILL IT BE ENOUGH?!"
    )


def test_event_creators(talker):
    se = talker.event_creators(336)
    assert len(se) == 20
    chuck = se[10]
    assert chuck.id == 13000
    assert chuck.full_name == "Charles Beacham"
    assert (
        chuck.thumbnail
        == "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg"
    )


def test_event_series(talker):
    se = talker.event_series(336)
    assert len(se) == 20
    champs = se[5]
    assert champs.id == 22552
    assert champs.start_year == 2016
    assert champs.end_year == 2019
    assert champs.title == "Champions (2016 - 2019)"


def test_event_stories(talker):
    se = talker.event_stories(336)
    assert len(se) == 20
    dp = se[1]
    assert dp.id == 109336
    assert dp.type == "story"
    assert len(dp.characters) == 0
    assert len(dp.comics) == 1
    assert len(dp.creators) == 3
    assert len(dp.events) == 2
    assert len(dp.series) == 1
    assert dp.original_issue.id == 48620
    assert dp.original_issue.name == "Deadpool (2012) #32"
