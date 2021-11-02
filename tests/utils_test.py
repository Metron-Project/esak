import pytest

from esak.utils import check_mod_date


def test_bad_modification_dates():
    good_data = {
        "id": 24393,
        "modified": "2018-04-09T11:21:09-0400",
    }
    data = check_mod_date(good_data)
    assert data["modified"] == "2018-04-09T11:21:09-0400"


def test_good_modiciation_date():
    bad_data = {"id": 1010774, "modified": "-0001-11-30T00:00:00-0500"}
    data = check_mod_date(bad_data)
    with pytest.raises(KeyError):
        data["modified"]
