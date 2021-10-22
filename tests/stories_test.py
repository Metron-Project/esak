"""
Test Stories module.

This module contains tests for Stories objects.
"""


def test_known_stories(talker):
    sm = talker.stories(35505)
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
