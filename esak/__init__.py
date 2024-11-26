"""Project entry file."""

__all__ = ["__version__", "api"]
__version__ = "2.0.0"

from esak.exceptions import AuthenticationError
from esak.session import Session
from esak.sqlite_cache import SqliteCache


def api(
    public_key: str | None = None, private_key: str | None = None, cache: SqliteCache | None = None
) -> Session:
    """Entry function the sets login credentials for Marvel's API.

    Args:
        public_key: The user's public key obtained from Marvel.
        private_key: The user's private key obtained from Marvel.
        cache: SqliteCache to use

    Returns:
        A session object

    Raises:
        AuthenticationError: If Marvel credentials are missing.
    """
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    return Session(public_key, private_key, cache=cache)
