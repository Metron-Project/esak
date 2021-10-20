"""
Test Comic module.
This module contains tests for Comic objects.
"""


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
    # assert af15.page_count == 36
    assert af15.id == 16926
    assert "Spider-Man (Peter Parker)" in [c.name for c in af15.characters]
    assert "Foo" not in [c.name for c in af15.characters]
    assert "Steve Ditko" in [s.name for s in af15.creators]
    assert "Abe Lincoln" not in [s.name for s in af15.creators]
    # assert af15.prices.print == 0.1


def test_invalid_isbn(talker):
    """Sometimes Marvel API sends number for isbn"""
    murpg = talker.comic(1143)
    assert murpg.isbn == "785110283"
    assert murpg.prices.print == 9.99


def test_invalid_diamond_code(talker):
    """Sometimes Marvel API sends number for diamond code"""
    hulk = talker.comic(27399)
    assert hulk.diamond_code == "0"


def test_upc_code(talker):
    cable = talker.comic(95781)
    assert cable.upc == "759606201991000111"
