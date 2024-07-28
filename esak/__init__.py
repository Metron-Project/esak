"""Project entry file."""

__version__ = "1.3.2"

from esak import exceptions, session, sqlite_cache


def api(
    public_key: str | None = None,
    private_key: str | None = None,
    cache: sqlite_cache.SqliteCache | None = None,
) -> session.Session:
    """Entry function the sets login credentials for Marvel's API.

    Parameters
    ----------
    public_key: str, optional
        The user's public key obtained from Marvel.
    private_key: str, optional
        The user's private key obtained from Marvel.
    cache: SqliteCache, optional
        SqliteCache to use

    Returns
    -------
    Session

    Raises
    ------
    AuthenticationError
        If Marvel credentials are missing.
    """
    if public_key is None:
        raise exceptions.AuthenticationError("Missing public_key.")

    if private_key is None:
        raise exceptions.AuthenticationError("Missing private_key.")

    return session.Session(public_key, private_key, cache=cache)
