"""Exceptions module.

This module provides the following classes:

- ApiError
- AuthenticationError
- CacheError
"""


class ApiError(Exception):
    """Class for any api errors."""


class AuthenticationError(ApiError):
    """Class for any authentication errors."""


class CacheError(ApiError):
    """Class for any database cache errors."""
