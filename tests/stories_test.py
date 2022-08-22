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
    assert (next(stories_iter).id) == 10670
    assert (next(stories_iter).id) == 59543
    assert (next(stories_iter).id) == 17283
    assert len(stories_lst) == 20
    assert stories_lst[2].id == 17283


def test_story_characters(talker):
    sm = talker.story_characters(35505)
    assert len(sm) == 1
    peter = sm[0]
    assert peter.id == 1009610
    assert peter.name == "Spider-Man (Peter Parker)"
    assert len(peter.comics) == 20
    assert len(peter.events) == 20
    assert len(peter.series) == 20
    assert len(peter.stories) == 20


def test_story_comics(talker):
    sm = talker.story_comics(35505)
    assert len(sm) == 2
    af = sm[1]
    assert af.id == 16926
    assert af.format == "Comic"
    assert af.issue_number == 15
    assert af.title == "Amazing Fantasy (1962) #15"


def test_story_creators(talker):
    sm = talker.story_creators(35505)
    assert len(sm) == 4
    ditko = sm[0]
    assert ditko.id == 32
    assert ditko.full_name == "Steve Ditko"
    assert len(ditko.comics) == 20
    assert len(ditko.events) == 1
    assert len(ditko.series) == 20
    assert len(ditko.stories) == 20


def test_story_events(talker):
    sm = talker.story_events(113981)
    assert len(sm) == 1
    sw = sm[0]
    assert sw.id == 323
    assert sw.title == "Secret Wars (2015)"
    assert sw.next.id == 332
    assert sw.previous.id == 321


def test_story_series(talker):
    sm = talker.story_series(35505)
    assert len(sm) == 2
    af = sm[0]
    assert af.id == 2987
    assert af.start_year == 1962
    assert af.end_year == 1962
    assert af.title == "Amazing Fantasy (1962)"
