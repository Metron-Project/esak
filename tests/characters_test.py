"""Test Characters module.

This module contains tests for Character objects.
"""

from datetime import date

from esak.session import Session


def test_known_character(talker: Session) -> None:
    """Test character endpoint with a known character."""
    cap = talker.character(1009220)
    assert cap.name == "Captain America"
    assert cap.resource_uri.__str__() == "http://gateway.marvel.com/v1/public/characters/1009220"
    assert (
        cap.thumbnail.__str__() == "http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087.jpg"
    )
    assert len(cap.series) > 0
    assert len(cap.events) > 0
    assert len(cap.stories) == 20
    assert cap.stories[0].id == 670
    assert cap.stories[0].name == "X-MEN (2004) #186"
    assert cap.stories[0].type == "cover"
    assert cap.stories[19].id == 1606
    assert cap.stories[19].name == "WEAPON X (2002) #14"
    assert cap.stories[19].type == "cover"

    assert len(cap.comics) == 20
    assert cap.comics[0].id == 43488
    assert cap.comics[0].name == "A+X (2012) #1"
    assert (
        cap.comics[0].resource_uri.__str__() == "http://gateway.marvel.com/v1/public/comics/43488"
    )

    assert len(cap.series) == 20
    assert cap.series[10].id == 9865
    assert cap.series[10].name == "All-Winners Squad: Band of Heroes (2011)"
    assert (
        cap.series[10].resource_uri.__str__() == "http://gateway.marvel.com/v1/public/series/9865"
    )


# def test_bad_character(talker: Session) -> None:
#     """Test character endpoint with a bad character."""
#     with pytest.raises(ApiError):
#         talker.character(-1)


def test_pulls_verbose(talker: Session) -> None:
    """Test character list endpoint."""
    characters = talker.characters_list({"orderBy": "modified"})

    c_iter = iter(characters)
    assert next(c_iter).name == "Prowler (Rick Lawson)"
    assert next(c_iter).name == "Ted Forrester"
    assert next(c_iter).name == "Hedge Knight"
    assert len(characters) > 0
    assert characters[1].name == "Ted Forrester"


def test_character_comics(talker: Session) -> None:
    """Test character comics endpoint with a known character."""
    cap = talker.character_comics(1009220)
    assert len(cap) == 20
    af2 = cap[2]
    assert af2.id == 116133
    assert af2.title == "Captain America (2023) #13"
    assert af2.issue_number == "13"
    assert af2.page_count == 32
    assert af2.upc == "75960620740401311"
    assert af2.format == "Comic"
    assert af2.series.id == 37724
    assert af2.series.name == "Captain America (2023 - Present)"
    assert af2.series.resource_uri.__str__() == "http://gateway.marvel.com/v1/public/series/37724"
    assert af2.dates.foc == date(2024, 8, 12)
    assert af2.dates.on_sale == date(2024, 9, 11)
    assert len(af2.stories) == 2
    assert len(af2.events) == 0
    assert len(af2.creators) == 6


def test_character_events(talker: Session) -> None:
    """Test character events endpoint with a known character."""
    cap = talker.character_events(1009220)
    assert len(cap) == 20
    fall = cap[9]
    assert fall.id == 248
    assert fall.title == "Fall of the Mutants"
    assert (
        fall.thumbnail.__str__() == "http://i.annihil.us/u/prod/marvel/i/mg/8/a0/51cb2f521ae35.jpg"
    )
    assert fall.start == date(1988, 1, 10)
    assert fall.end == date(2007, 1, 17)
    assert fall.next.id == 252
    assert fall.next.name == "Inferno"
    assert fall.previous.id == 246
    assert fall.previous.name == "Evolutionary War"


def test_character_series(talker: Session) -> None:
    """Test character series endpoint with a known character."""
    cap = talker.character_series(1009220)
    assert len(cap) == 20
    af = cap[12]
    assert af.title == "Amazing Fantasy (2021)"
    assert af.id == 25984
    assert af.start_year == 2021
    assert af.end_year == 2021
    assert len(af.comics) == 16
    assert len(af.characters) == 3
    assert len(af.creators) == 10
    assert af.next is None
    assert af.previous is None


def test_character_stories(talker: Session) -> None:
    """Test character stories endpoint with a known character."""
    cap = talker.character_stories(1009220)
    assert len(cap) == 20
    av_503 = cap[5]
    assert av_503.id == 1042
    assert av_503.title == "Avengers (1998) #503"
    assert av_503.type == "cover"
    assert len(av_503.characters) == 1
    assert len(av_503.comics) == 1
    assert len(av_503.creators) == 0
    assert av_503.original_issue.id == 923
    assert av_503.original_issue.name == "Avengers (1998) #503"
    assert (
        av_503.original_issue.resource_uri.__str__()
        == "http://gateway.marvel.com/v1/public/comics/923"
    )
