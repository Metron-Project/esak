# esak - Python wrapper for Marvel API

[![PyPI - Python](https://img.shields.io/pypi/pyversions/esak.svg?logo=Python&label=Python&style=flat-square)](https://pypi.python.org/pypi/esak/)
[![PyPI - Version](https://img.shields.io/pypi/v/esak.svg?logo=Python&label=Version&style=flat-square)](https://pypi.python.org/pypi/esak/)
[![PyPI - License](https://img.shields.io/pypi/l/esak.svg?logo=Python&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

[![Github - Contributors](https://img.shields.io/github/contributors/Metron-Project/esak.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Metron-Project/esak/graphs/contributors)
[![Github Action - Testing](https://img.shields.io/github/actions/workflow/status/Metron-Project/esak/testing.yml?branch=master&logo=Github&label=Testing&style=flat-square)](https://github.com/Metron-Project/esak/actions/workflows/testing.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/Metron-Project/esak?token=L1EGNX24I2&logo=codecov&label=Codecov&style=flat-square)](https://codecov.io/gh/Metron-Project/esak)

[![Read the Docs](https://img.shields.io/readthedocs/esak?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://esak.readthedocs.io/en/stable)

This project is a fork of [marvelous](https://github.com/rkuykendall/marvelous) with the goal of supporting the full Marvel API.

## Installation

```console
pip install --user esak
```

## Example Usage

```python
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
    # Write a line to the file with the name of the issue, and the id of the series
    print(f'{comic.title} (series #{comic.series.id})')
```

## Documentation

- [esak](https://esak.readthedocs.io/en/stable)
- [Marvel API](https://developer.marvel.com/docs)

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/Metron-Project/esak/issues) to submit bugs or request features.

## Contributing

- When running a new test for the first time, set the environment variables `PUBLIC_KEY` and `PRIVATE_KEY` to your Marvel API keys.
  The responses will be cached in the `tests/testing_mock.sqlite` database without your keys.

## Socials

[![Social - Matrix](https://img.shields.io/matrix/metron-general:matrix.org?label=Metron%20General&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-general:matrix.org)
[![Social - Matrix](https://img.shields.io/matrix/metron-devel:matrix.org?label=Metron%20Development&logo=matrix&style=for-the-badge)](https://matrix.to/#/#metron-development:matrix.org)
