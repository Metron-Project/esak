Introduction
------------

Esak was created to make it easy to write small but powerful scripts which
leverage the Marvel API, such as reading lists. The original use was to
automate a list of Marvel comics weekly releases without having to copy each
title manually from the Midtown Comics website.

This package uses 2 major libraries :

- requests for connecting to the Marvel API
- marshmallow for parsing the response into python objects

Instantiating API
-----------------

.. code-block:: python

    import esak

    # Authenticate with Marvel, with keys from https://developer.marvel.com/
    e = esak.api(public_key, private_key)

    # Get all Marvel comics for the week of 2021-06-07
    this_week = e.comics_list({"dateDescriptor": "thisWeek"})

    # Print the results
    for i in this_week:
        print(f"{i.id} {i.title}")

    # Retrieve the detail for an individual comic
    af15 = e.comic(16926)

    # Print some of the comic's information
    print(f"{af15.id} ({af15.format}): {af15.title}")
