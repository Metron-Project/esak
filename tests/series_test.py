"""
Test Series module.
This module contains tests for Series objects.
"""
import datetime
from decimal import Decimal

import pytest

from esak import comic, exceptions
from esak.series import Series


def test_known_series(talker):

    usms = talker.series(466)
    assert usms.title == "Ultimate Spider-Man (2000 - 2009)"
    assert usms.id == 466
    assert usms.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/6/c0/5149db8019dc9.jpg"
    assert usms.end_year == 2009
    assert usms.start_year == 2000
    assert usms.modified == datetime.datetime(
        2013,
        3,
        20,
        11,
        54,
        44,
        tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)),
    )
    assert usms.description == (
        "In 2000, Marvel embarked on a bold new experiment, re-imagining some "
        "of their greatest heroes in the 21st century, beginning with Spider-Man! "
        "Writer Brian Michael Bendis along with artists Mark Bagley and Stuart Immonen "
        "invite you to discover the world of Peter Parker in a whole new way with the "
        "series that changed everything!"
    )
    assert usms.rating == "A"

    assert len(usms.comics) == 20
    assert usms.comics[0].id == 4372
    assert usms.comics[0].name == "Ultimate Spider-Man (2000) #1"
    assert usms.comics[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/4372"

    assert len(usms.characters) == 20
    assert usms.characters[11].id == 1010921
    assert usms.characters[11].name == "Doctor Octopus (Ultimate)"
    assert usms.characters[11].role is None
    assert (
        usms.characters[11].resource_uri
        == "http://gateway.marvel.com/v1/public/characters/1010921"
    )

    assert len(usms.creators) == 20
    assert usms.creators[12].id == 162
    assert usms.creators[12].name == "John Cassaday"
    assert usms.creators[12].role == "penciller"
    assert usms.creators[12].resource_uri == "http://gateway.marvel.com/v1/public/creators/162"


def test_bad_series(talker):
    with pytest.raises(exceptions.ApiError):
        talker.series(-1)


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        comic.ComicsList({"data": {"results": [{"modified": "potato"}]}})


def test_all_series(talker):
    # check known values
    usm = talker.series_list(
        params={"title": "Ultimate Spider-Man"}
    )  # don't include '(year - year)', it doesn't work
    assert usm is not None
    assert len(usm) == 1
    assert isinstance(usm[0], Series)
    # check the filter works returning multiple items
    series_iter = talker.series_list(
        params={"seriesType": "ongoing", "startYear": 2009, "limit": 10}
    )
    powers = series_iter[7]
    assert powers.id == 9073
    assert powers.start_year == 2009
    assert powers.end_year == 2012
    assert powers.title == "Powers (2009 - 2012)"
    assert powers.type == "ongoing"
    assert powers.resource_uri == "http://gateway.marvel.com/v1/public/series/9073"


def test_pulls_verbose(talker):
    series = talker.series_list()
    s_iter = iter(series)
    assert next(s_iter).id == 31445
    assert next(s_iter).id == 26024
    assert next(s_iter).id == 18454
    assert len(series) > 0
    assert series[1].id == 26024


def test_series_characters(talker):
    sm = talker.series_characters(24396)
    assert len(sm.character) == 20
    kingpin = sm.character[12]
    assert kingpin.id == 1009389
    assert kingpin.name == "Kingpin"
    assert kingpin.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/9/60/526034fb5aff7.jpg"
    assert len(kingpin.comics) == 20
    assert len(kingpin.events) == 7
    assert len(kingpin.series) == 20
    assert len(kingpin.stories) == 20
    assert kingpin.urls.onsale_date is None


def test_series_comics(talker):
    sm = talker.series_comics(24396)
    assert len(sm.comics) == 20
    sm_75 = sm.comics[1]
    assert sm_75.format == "Comic"
    assert sm_75.title == "The Amazing Spider-Man (2018) #93"
    assert sm_75.issue_number == 93
    assert sm_75.page_count == 56
    assert sm_75.resource_uri == "http://gateway.marvel.com/v1/public/comics/96827"
    assert sm_75.upc == "75960608936909311"
    assert len(sm_75.creators) == 11
    assert len(sm_75.characters) == 2
    assert len(sm_75.events) == 0
    assert len(sm_75.stories) == 2
    assert sm_75.prices.print == Decimal("5.99")
    assert sm_75.prices.digital is None


def test_series_creators(talker):
    sm = talker.series_creators(24396)
    assert len(sm.creator) == 20
    bagley = sm.creator[12]
    assert bagley.id == 87
    assert bagley.first_name == "Mark"
    assert bagley.last_name == "Bagley"
    assert bagley.full_name == "Mark Bagley"
    assert bagley.resource_uri == "http://gateway.marvel.com/v1/public/creators/87"
    assert bagley.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/9/b0/4bc5d2f67f706.jpg"
    assert len(bagley.comics) == 20
    assert len(bagley.events) == 13
    assert len(bagley.series) == 20
    assert len(bagley.stories) == 20


def test_series_events(talker):
    AvX = talker.series_events(15305)
    assert len(AvX.events) == 1
    e = AvX[0]
    assert e.id == 310
    assert e.title == "Avengers VS X-Men"
    assert e.resource_uri == "http://gateway.marvel.com/v1/public/events/310"
    assert e.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/3/20/5109a1f93b543.jpg"
    assert len(e.characters) == 20
    assert len(e.comics) == 20
    assert len(e.creators) == 20
    assert len(e.series) == 9
    assert len(e.stories) == 20
    assert e.start == datetime.date(2012, 4, 4)
    assert e.end == datetime.date(2012, 9, 19)
    assert e.next.id == 311
    assert e.next.name == "Marvel NOW!"
    assert e.next.resource_uri == "http://gateway.marvel.com/v1/public/events/311"
    assert e.previous.id == 309
    assert e.previous.name == "Shattered Heroes"
    assert e.previous.resource_uri == "http://gateway.marvel.com/v1/public/events/309"


def test_series_stories(talker):
    AvX = talker.series_stories(15305)
    assert len(AvX.stories) == 20
    s = AvX.stories[13]
    assert s.id == 93246
    assert s.type == "story"
    assert s.resource_uri == "http://gateway.marvel.com/v1/public/stories/93246"
    assert len(s.characters) == 4
    assert len(s.comics) == 1
    assert len(s.creators) == 6
    assert len(s.events) == 1
    assert len(s.series) == 1
    assert s.original_issue.id == 41193
    assert s.original_issue.name == "Avengers Vs. X-Men (2012) #4"
    assert s.original_issue.resource_uri == "http://gateway.marvel.com/v1/public/comics/41193"
