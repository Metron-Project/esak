"""SQLite Cache module.

This module provides the following classes:

- SqliteCache
"""

__all__ = ["SqliteCache"]
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any


class SqliteCache:
    """The SqliteCache object to cache search results from Marvel.

    Args:
        db_name: Path and database name to use.
        expire: The number of days to keep the cache results before they expire.
    """

    def __init__(self, db_name: str = "esak_cache.db", expire: int | None = None) -> None:
        self.expire = expire
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS responses (key, json, expire)")
        self.cleanup()

    def get(self, key: str) -> Any | None:  # noqa: ANN401
        """Retrieve data from the cache database.

        Args:
            key: Value to search for.

        Returns:
            Selected results or None
        """
        self.cur.execute("SELECT json FROM responses WHERE key = ?", (key,))
        return json.loads(result[0]) if (result := self.cur.fetchone()) else None

    def store(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Save data to the cache database.

        Args:
            key: Item id.
            value: Data to save.
        """
        self.cur.execute(
            "INSERT INTO responses(key, json, expire) VALUES(?, ?, ?)",
            (key, json.dumps(value), self._determine_expire_str()),
        )
        self.con.commit()

    def cleanup(self) -> None:
        """Remove any expired data from the cache database."""
        if not self.expire:
            return
        self.cur.execute(
            "DELETE FROM responses WHERE expire < ?;", (datetime.now().strftime("%Y-%m-%d"),)
        )
        self.con.commit()

    def _determine_expire_str(self) -> str:
        dt = datetime.now() + timedelta(days=self.expire) if self.expire else datetime.now()
        return dt.strftime("%Y-%m-%d")
