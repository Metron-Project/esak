esak - Marvel API wrapper for python 3
===========================================


.. image:: https://img.shields.io/pypi/v/esak.svg?logo=PyPI&label=Version&style=flat-square   :alt: PyPI
    :target: https://pypi.org/project/esak

.. image:: https://img.shields.io/pypi/pyversions/esak.svg?logo=Python&label=Python-Versions&style=flat-square
    :target: https://pypi.org/project/esak

.. image:: https://img.shields.io/github/license/bpepple/esak
    :target: https://opensource.org/licenses/GPL-3.0

.. image:: https://codecov.io/gh/bpepple/esak/branch/master/graph/badge.svg?token=L1EGNX24I2
    :target: https://codecov.io/gh/bpepple/esak

.. image:: https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=flat-square
    :target: https://github.com/psf/black

- `Code on Github <https://github.com/bpepple/esak>`_
- `Published on PyPi <https://pypi.python.org/pypi/esak>`_
- `Marvel API documentation <https://developer.marvel.com/docs>`_

**To install:**

.. code-block:: bash

    $ pip3 install --user esak
 
**Example Usage:**

.. code-block:: python

    import esak

    # Your own config file to keep your private key local and secret
    from config import public_key, private_key

    # Authenticate with Marvel, with keys I got from http://developer.marvel.com/
    m = esak.api(public_key, private_key)

    # Get all comics from this week, sorted alphabetically by title
    pulls = sorted(m.comics_list({
        'format': "comic",
        'formatType': "comic",
        'noVariants': True,
        'dateDescriptor': "thisWeek",
        'limit': 100}),
        key=lambda comic: comic.title)

    for comic in pulls:
        # Write a line to the file with the name of the issue, and the
        # id of the series
        print('{} (series #{})'.format(comic.title, comic.series.id))

Documentation
-------------
- `Read the project documentation <https://esak.readthedocs.io/en/stable/>`_

Bugs/Requests
-------------
  
Please use the `GitHub issue tracker <https://github.com/bpepple/esak/issues>`_ to submit bugs or request features.

Contributing
------------

- When running a new test for the first time, set the environment variables
  ``PUBLIC_KEY`` and ``PRIVATE_KEY`` to any Marel API keys. The result will be
  stored in the `tests/testing_mock.sqlite` database without your keys.

