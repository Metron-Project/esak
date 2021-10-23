"""
Test Series module.
This module contains tests for Series objects.
"""
import datetime

import pytest

from esak import comics_list, exceptions
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


def test_bad_series(talker):
    with pytest.raises(exceptions.ApiError):
        talker.series(-1)


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        comics_list.ComicsList({"data": {"results": [{"modified": "potato"}]}})


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
    for s in series_iter:
        assert isinstance(s, Series)
        assert s.start_year == 2009


def test_pulls_verbose(talker):
    series = talker.series_list()
    s_iter = iter(series)
    assert next(s_iter).id == 31445
    assert next(s_iter).id == 26024
    assert next(s_iter).id == 18454
    assert len(series) > 0
