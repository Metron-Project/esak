"""
Test Comic module.
This module contains tests for Comic objects.
"""
from decimal import Decimal


def test_pulls_verbose(talker):
    week = talker.comics_list(
        {
            "format": "comic",
            "formatType": "comic",
            "noVariants": True,
            "dateDescriptor": "thisWeek",
        }
    )
    c_iter = iter(week)
    assert next(c_iter).id == 89738
    assert next(c_iter).id == 93316
    assert next(c_iter).id == 93320
    assert len(week) > 0


def test_pulls_simple(talker):
    week = talker.comics_list({"dateDescriptor": "thisWeek"})
    assert len(week.comics) > 0


def test_pulls_simpler(talker):
    week = talker.comics_list()
    assert len(week.comics) > 0


def test_known_comic(talker):
    af15 = talker.comic(16926)
    assert af15.title == "Amazing Fantasy (1962) #15"
    assert af15.issue_number == 15
    assert af15.description is None
    assert af15.format == "Comic"
    assert af15.id == 16926
    assert "Spider-Man (Peter Parker)" in [c.name for c in af15.characters]
    assert "Foo" not in [c.name for c in af15.characters]
    assert "Steve Ditko" in [s.name for s in af15.creators]
    assert "Abe Lincoln" not in [s.name for s in af15.creators]
    assert af15.prices.print == Decimal("0.00")
    assert len(af15.stories) == 5
    assert af15.stories[0].id == 35504
    assert af15.stories[0].type == "cover"
    assert af15.stories[0].name == "Cover: Amazing Fantasy (1962) #15"
    assert af15.stories[1].id == 35505
    assert af15.stories[1].type == "interiorStory"
    assert af15.stories[1].name == "Spider-Man!"
    assert af15.stories[2].id == 35506
    assert af15.stories[2].type == "interiorStory"
    assert af15.stories[2].name == "The Bell-Ringer"


def test_invalid_isbn(talker):
    """Sometimes Marvel API sends number for isbn"""
    murpg = talker.comic(1143)
    assert murpg.isbn == "785110283"
    assert murpg.prices.print == Decimal("9.99")


def test_invalid_diamond_code(talker):
    """Sometimes Marvel API sends number for diamond code"""
    hulk = talker.comic(27399)
    assert hulk.diamond_code == "0"


def test_upc_code(talker):
    cable = talker.comic(95781)
    assert cable.upc == "759606201991000111"


def test_comic_digital_price(talker):
    cw1 = talker.comic(4216)
    assert cw1.title == "Civil War (2006) #1"
    assert cw1.prices.print == Decimal("0.00")
    assert cw1.prices.digital == Decimal("1.99")
    assert cw1.series.name == "Civil War (2006 - 2007)"
    assert cw1.format == "Comic"
    assert cw1.upc == "75960605921800111"
    assert cw1.issue_number == 1
    assert cw1.digital_id == 5486
    assert len(cw1.stories) == 2
    assert cw1.stories[0].id == 5872
    assert cw1.stories[0].type == "cover"
    assert cw1.stories[0].name == "1 of 7 - 7XLS"
    assert cw1.stories[1].id == 5873
    assert cw1.stories[1].type == "interiorStory"
    assert cw1.stories[1].name == "1 of 7 - 7XLS"
