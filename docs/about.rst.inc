**Esak** is a python wrapper for the Marvel API.

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