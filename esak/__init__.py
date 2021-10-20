"""Project entry file."""
__version__ = "1.0.0"

from typing import Optional

from esak import exceptions, session, sqlite_cache


def api(
    public_key: Optional[str] = None,
    private_key: Optional[str] = None,
    cache: Optional[sqlite_cache.SqliteCache] = None,
) -> session.Session:
    """Entry function the sets login credentials for Marvel's API.

    :param public_key: The username used for metron.cloud.
    :type public_key: str, optional
    :param private_key: The password used for metron.cloud.
    :type private_key: str, optional
    :param cache: SqliteCache to use
    :type cache: SqliteCache, optional
    """
    if public_key is None:
        raise exceptions.AuthenticationError("Missing public_key.")

    if private_key is None:
        raise exceptions.AuthenticationError("Missing private_key.")

    return session.Session(public_key, private_key, cache=cache)
