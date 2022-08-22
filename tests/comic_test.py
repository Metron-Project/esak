"""
Test Comic module.
This module contains tests for Comic objects.
"""
from datetime import date, datetime
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
    assert next(c_iter).id == 95836
    assert next(c_iter).id == 98687
    assert next(c_iter).id == 95855
    assert len(week) > 0
    assert week[1].id == 98687


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
    assert af15.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/f/10/598363848588e.jpg"
    assert "Spider-Man (Peter Parker)" in [c.name for c in af15.characters]
    assert "Foo" not in [c.name for c in af15.characters]
    assert "Steve Ditko" in [s.name for s in af15.creators]
    assert "Abe Lincoln" not in [s.name for s in af15.creators]
    assert af15.prices.print == Decimal("0.00")
    assert af15.prices.digital is None
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
    assert af15.dates.on_sale == date(1962, 8, 1)
    assert af15.dates.foc is None
    assert af15.dates.unlimited == date(2008, 5, 13)
    assert len(af15.collections) == 1
    assert af15.collections[0].id == 16214
    assert af15.collections[0].name == "AMAZING FANTASY OMNIBUS HC (Hardcover)"
    assert (
        af15.collections[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/16214"
    )
    assert len(af15.collected_issues) < 1
    assert len(af15.variants) < 1
    assert len(af15.text_objects) == 1
    assert af15.text_objects[0].type == "70th_winner_desc"
    assert af15.text_objects[0].language == "en-us"
    assert (
        af15.text_objects[0].text
        == "Jack Kirby and Steve Ditko collaborated on this cover to create what "
        "is quite possibly the most iconic image in Marvel Comics' history.  Before "
        "all the clones, symbiotes and civil wars we see Spider-Man in a simpler time "
        "doing what he does best, catching crooks and saving the day."
    )


def test_invalid_isbn(talker):
    """Sometimes Marvel API sends number for isbn"""
    murpg = talker.comic(1143)
    assert murpg.isbn == "785110283"
    assert murpg.prices.print == Decimal("9.99")
    assert murpg.prices.digital is None


def test_invalid_diamond_code(talker):
    """Sometimes Marvel API sends number for diamond code"""
    hulk = talker.comic(27399)
    assert hulk.diamond_code == "0"


def test_upc_code(talker):
    cable = talker.comic(95781)
    assert cable.upc == "759606201991000111"
    assert cable.dates.on_sale == date(2021, 8, 25)
    assert cable.dates.foc == date(2021, 8, 2)
    assert cable.dates.unlimited == date(2021, 11, 29)


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
    assert cw1.dates.on_sale == date(2006, 5, 3)
    assert cw1.dates.foc is None
    assert cw1.dates.unlimited == date(2009, 8, 12)
    assert cw1.images[0] == "http://i.annihil.us/u/prod/marvel/i/mg/e/f0/511307b2f1200.jpg"
    assert cw1.images[1] == "http://i.annihil.us/u/prod/marvel/i/mg/6/f0/4f75b393338cf.jpg"


def test_comic_characters(talker):
    a1 = talker.comic_characters(67002)
    assert len(a1.character) == 9
    she_hulk = a1.character[7]
    assert she_hulk.id == 1009583
    assert she_hulk.name == "She-Hulk (Jennifer Walters)"
    assert she_hulk.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009583"
    assert (
        she_hulk.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/7/20/527bb5d64599e.jpg"
    )
    assert len(she_hulk.comics) == 20
    assert len(she_hulk.events) == 15
    assert len(she_hulk.series) == 20
    assert len(she_hulk.stories) == 20


def test_comic_creators(talker):
    a1 = talker.comic_creators(67002)
    assert len(a1.creator) > 0
    jason = a1.creator[0]
    assert jason.id == 11463
    assert jason.first_name == "Jason"
    assert jason.last_name == "Aaron"
    assert jason.full_name == "Jason Aaron"
    assert jason.resource_uri == "http://gateway.marvel.com/v1/public/creators/11463"
    assert jason.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/7/10/5cd9c7870670e.jpg"
    assert len(jason.comics) == 20
    assert len(jason.events) == 10
    assert len(jason.series) == 20
    assert len(jason.stories) == 20


def test_comic_events(talker):
    sw1 = talker.comic_events(52447)
    assert len(sw1.events) == 1
    secret_wars = sw1.events[0]
    assert secret_wars.id == 323
    assert secret_wars.title == "Secret Wars (2015)"
    assert (
        secret_wars.thumbnail
        == "http://i.annihil.us/u/prod/marvel/i/mg/c/70/545be45c5d6cc.jpg"
    )
    assert secret_wars.resource_uri == "http://gateway.marvel.com/v1/public/events/323"
    assert secret_wars.start == date(2015, 5, 1)
    assert secret_wars.end == date(2015, 12, 31)
    assert len(secret_wars.characters) == 9
    assert len(secret_wars.comics) == 20
    assert len(secret_wars.creators) == 20
    assert len(secret_wars.series) == 20
    assert secret_wars.next.id == 332
    assert secret_wars.next.name == "Dead No More: The Clone Conspiracy"
    assert secret_wars.next.resource_uri == "http://gateway.marvel.com/v1/public/events/332"
    assert secret_wars.previous.id == 321
    assert secret_wars.previous.name == "Spider-Verse"
    assert (
        secret_wars.previous.resource_uri == "http://gateway.marvel.com/v1/public/events/321"
    )


def test_comic_stories(talker):
    aforce4 = talker.comic_stories(51206)
    assert len(aforce4.stories) == 2
    s = aforce4.stories[1]
    assert s.id == 113990
    assert s.type == "story"
    assert s.resource_uri == "http://gateway.marvel.com/v1/public/stories/113990"
    assert len(s.characters) == 0
    assert len(s.comics) == 1
    assert len(s.creators) == 3
    assert len(s.events) == 1
    assert s.original_issue.id == 51206
    assert s.original_issue.name == "A-Force (2015) #4"
    assert s.original_issue.resource_uri == "http://gateway.marvel.com/v1/public/comics/51206"
    assert len(s.series) == 1
    assert s.thumbnail is None
