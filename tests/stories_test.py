"""
Test Stories module.

This module contains tests for Stories objects.
"""
import pytest

from esak import exceptions


def test_known_story(talker):
    sm = talker.story(35505)
    assert sm.title == "Spider-Man!"
    assert sm.type == "story"
    assert sm.thumbnail is None

    assert sm.creators[0].name == "Steve Ditko"
    assert sm.creators[0].resource_uri == "http://gateway.marvel.com/v1/public/creators/32"
    assert sm.creators[0].role == "inker"
    assert sm.creators[1].name == "Stan Goldberg"
    assert sm.creators[1].role == "colorist"
    assert sm.creators[1].resource_uri == "http://gateway.marvel.com/v1/public/creators/962"

    assert len(sm.events) == 0

    assert sm.series[0].name == "Amazing Fantasy (1962)"
    assert sm.series[0].resource_uri == "http://gateway.marvel.com/v1/public/series/2987"
    assert sm.series[1].name == "AMAZING FANTASY OMNIBUS HC (2007)"
    assert sm.series[1].resource_uri == "http://gateway.marvel.com/v1/public/series/2707"

    assert sm.original_issue.id == 16926
    assert sm.original_issue.name == "Amazing Fantasy (1962) #15"
    assert sm.original_issue.resource_uri == "http://gateway.marvel.com/v1/public/comics/16926"

    assert sm.characters[0].id == 1009610
    assert sm.characters[0].name == "Spider-Man (Peter Parker)"
    assert (
        sm.characters[0].resource_uri
        == "http://gateway.marvel.com/v1/public/characters/1009610"
    )

    assert len(sm.comics) == 2
    assert sm.comics[0].id == 16926
    assert sm.comics[0].name == "Amazing Fantasy (1962) #15"
    assert sm.comics[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/16926"

    assert len(sm.characters) == 1
    assert sm.characters[0].id == 1009610
    assert sm.characters[0].name == "Spider-Man (Peter Parker)"
    assert sm.characters[0].role is None
    assert (
        sm.characters[0].resource_uri
        == "http://gateway.marvel.com/v1/public/characters/1009610"
    )


def test_bad_story(talker):
    with pytest.raises(exceptions.ApiError):
        talker.story(-1)


def test_stories_list(talker):
    stories_lst = talker.stories_list(
        {
            "orderBy": "modified",
        }
    )

    stories_iter = iter(stories_lst)
    assert (next(stories_iter).id) == 32039
    assert (next(stories_iter).id) == 41777
    assert (next(stories_iter).id) == 8186
    assert len(stories_lst) == 20
