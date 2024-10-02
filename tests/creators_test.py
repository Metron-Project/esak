"""Test Creator module.

This module contains tests for Creator objects.
"""

from datetime import date
from decimal import Decimal

import pytest

from esak.exceptions import ApiError
from esak.session import Session


def test_known_creator(talker: Session) -> None:
    """Test creator endpoint with a known creator."""
    jason = talker.creator(11463)
    assert jason.first_name == "Jason"
    assert jason.last_name == "Aaron"
    assert jason.id == 11463
    assert (
        jason.thumbnail.__str__() == "http://i.annihil.us/u/prod/marvel/i/mg/7/10/5cd9c7870670e.jpg"
    )

    assert 16450 in [s.id for s in jason.series]
    assert len(jason.series[:5]) == 5
    assert len(jason.series) == len([x for x in jason.series if x.id > 3])

    assert len(jason.stories) == 20
    assert jason.stories[0].id == 32907
    assert jason.stories[0].name == "Man In The Pit 1 of 1"
    assert jason.stories[0].type == "interiorStory"
    assert (
        jason.stories[0].resource_uri.__str__()
        == "http://gateway.marvel.com/v1/public/stories/32907"
    )

    assert len(jason.comics) == 20
    assert jason.comics[0].id == 45762
    assert jason.comics[0].name == "A+X Vol. 1: = Awesome (Trade Paperback)"
    assert (
        jason.comics[0].resource_uri.__str__() == "http://gateway.marvel.com/v1/public/comics/45762"
    )

    assert len(jason.series) == 20
    assert jason.series[11].id == 24229
    assert jason.series[11].name == "Avengers (2018 - 2023)"
    assert (
        jason.series[11].resource_uri.__str__()
        == "http://gateway.marvel.com/v1/public/series/24229"
    )


def test_bad_creator(talker: Session) -> None:
    """Test creator endpoint with a bad creator."""
    with pytest.raises(ApiError):
        talker.creator(-1)


def test_pulls_verbose(talker: Session) -> None:
    """Test creator list endpoint."""
    creators = talker.creators_list({"orderBy": "modified"})
    c_iter = iter(creators)
    assert next(c_iter).full_name == "Miles Lane"
    assert next(c_iter).full_name == "Christopher Moeller"
    assert next(c_iter).full_name == "Carlos D'anda"
    assert len(creators) > 0
    assert creators[1].full_name == "Christopher Moeller"


def test_creator_comics(talker: Session) -> None:
    """Test creator comics endpoint with a known creator."""
    jason = talker.creator_comics(11463)
    assert len(jason) == 20
    val5 = jason[6]
    assert val5.id == 120971
    assert val5.series.id == 37818
    assert val5.series.name == "Namor (2024 - Present)"
    assert val5.series.resource_uri.__str__() == "http://gateway.marvel.com/v1/public/series/37818"
    assert val5.title == "Namor (2024) #2 (Variant)"
    assert val5.issue_number == "2"
    assert val5.page_count == 40
    assert val5.upc == "75960620743500231"
    assert val5.format == "Comic"
    assert len(val5.characters) == 0
    assert len(val5.creators) == 8
    assert len(val5.events) == 0
    assert len(val5.stories) == 2
    assert val5.prices.digital is None
    assert val5.prices.print == Decimal("4.99")
    assert val5.dates.on_sale == date(2024, 8, 21)
    assert val5.dates.foc == date(2024, 7, 22)


def test_creator_events(talker: Session) -> None:
    """Test creator events endpoint with a known creator."""
    jason = talker.creator_events(11463)
    assert len(jason) == 10
    s = jason[5]
    assert s.id == 309
    assert s.title == "Shattered Heroes"
    assert s.thumbnail.__str__() == "http://i.annihil.us/u/prod/marvel/i/mg/2/a0/511e8000770cd.jpg"
    assert s.resource_uri.__str__() == "http://gateway.marvel.com/v1/public/events/309"
    assert len(s.characters) == 20
    assert len(s.comics) == 20
    assert len(s.creators) == 20
    assert len(s.series) == 10
    assert len(s.stories) == 20
    assert s.start == date(2011, 10, 19)
    assert s.end == date(2012, 4, 22)


def test_creator_series(talker: Session) -> None:
    """Test creator series endpoint with a known creator."""
    jason = talker.creator_series(11463)
    assert len(jason) == 20
    ax = jason[0]
    assert ax.id == 16450
    assert ax.start_year == 2012
    assert ax.end_year == 2014
    assert ax.title == "A+X (2012 - 2014)"
    assert ax.next is None
    assert ax.previous is None


def test_creator_stories(talker: Session) -> None:
    """Test creator stories endpoint with a known creator."""
    jason = talker.creator_stories(11463)
    assert len(jason) == 20
    man = jason[0]
    assert man.id == 32907
    assert man.title == "Man In The Pit 1 of 1"
    assert man.type == "story"
    assert man.resource_uri.__str__() == "http://gateway.marvel.com/v1/public/stories/32907"
    assert len(man.characters) == 2
    assert len(man.comics) == 1
    assert len(man.creators) == 4
    assert man.original_issue.id == 16112
    assert man.original_issue.name == "Wolverine (2003) #56"
