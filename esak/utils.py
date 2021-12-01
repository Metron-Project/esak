"""
Utils module.

This module provides the following functions:

- check_mod_date
"""


def check_mod_date(data):
    """
    Remove a bad modification date from json data.

    Parameters
    ----------
    data
        Data from a Marvel API response.
    """
    # Marvel comic 1768, and maybe others, returns a modified of
    # "-0001-11-30T00:00:00-0500". The best way to handle this is
    # probably just to ignore it, since I don't know how to fix it.
    if data.get("modified", " ")[0] == "-":
        del data["modified"]
    return data
