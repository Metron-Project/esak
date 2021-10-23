"""
Test Characters module.
This module contains tests for Character objects.
"""
import pytest

from esak import exceptions


def test_known_character(talker):
    cap = talker.character(1009220)
    assert cap.name == "Captain America"
    assert cap.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009220"
    assert cap.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087.jpg"
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
    assert cap.comics[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/43488"

    assert len(cap.series) == 20
    assert cap.series[10].id == 9865
    assert cap.series[10].name == "All-Winners Squad: Band of Heroes (2011)"
    assert cap.series[10].resource_uri == "http://gateway.marvel.com/v1/public/series/9865"


def test_bad_character(talker):
    with pytest.raises(exceptions.ApiError):
        talker.character(-1)


def test_pulls_verbose(talker):
    characters = talker.characters_list(
        {
            "orderBy": "modified",
        }
    )

    c_iter = iter(characters)
    assert (next(c_iter).name) == "Howard Saint"
    assert (next(c_iter).name) == "The Phantom"
    assert (next(c_iter).name) == "Nextwave"
    assert len(characters) > 0
