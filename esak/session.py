"""Session module.

This module provides the following classes:

- Session
"""

import platform
from collections import OrderedDict
from datetime import datetime
from hashlib import md5
from typing import Any
from urllib.parse import urlencode

import requests
from pydantic import TypeAdapter, ValidationError

from esak import __version__
from esak.exceptions import ApiError, CacheError
from esak.schemas.character import Character
from esak.schemas.comic import Comic
from esak.schemas.creator import Creator
from esak.schemas.event import Event
from esak.schemas.series import Series
from esak.schemas.story import Story
from esak.sqlite_cache import SqliteCache


class Session:
    """
    Session to request api endpoints.

    Parameters
    ----------
    public_key: str
        The public_key for authentication with Marvel
    private_key: str
        The private_key used for authentication with Marvel
    sqlite_cache.SqliteCache: optional, sqlite_cache.SqliteCache
        sqlite_cache.SqliteCache to use

    Returns
    -------
    Session
        A :class:`Session` object to make api calls to Marvel.
    """

    def __init__(self, public_key: str, private_key: str, cache: SqliteCache | None = None):
        """Initialize a new Session."""
        self.headers = {
            "User-Agent": f"esak/{__version__} ({platform.system()}; {platform.release()})"
        }
        self.public_key = public_key
        self.private_key = private_key
        self.cache = cache
        self.api_url = "http://gateway.marvel.com:80/v1/public/{}"

    @staticmethod
    def _create_cached_params(params: dict[str, Any]) -> str:
        # Generate part of cache key before hash, apikey and timestamp added
        cache_params = ""
        if params:
            ordered_params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
            cache_params = f"?{urlencode(ordered_params)}"
        return cache_params

    def _create_auth_hash(self, now_string: str) -> str:
        auth_hash = md5()
        auth_hash.update(now_string.encode("utf-8"))
        auth_hash.update(self.private_key.encode("utf-8"))
        auth_hash.update(self.public_key.encode("utf-8"))
        return auth_hash.hexdigest()

    def _update_params(self, params: dict[str, Any]) -> None:
        now_string = datetime.now().strftime("%Y-%m-%d%H:%M:%S")

        params["hash"] = self._create_auth_hash(now_string)
        params["apikey"] = self.public_key
        params["ts"] = now_string

    def _get_results_from_cache(self, key: str) -> Any | None:
        cached_response = None

        if self.cache:
            try:
                cached_response = self.cache.get(key)
                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise CacheError(
                    f"Cache object passed in is missing attribute: {repr(e)}"
                ) from e

        return cached_response

    def _save_results_to_cache(self, key: str, data: str) -> None:
        if self.cache:
            try:
                self.cache.store(key, data)
            except AttributeError as e:
                raise CacheError(
                    f"Cache object passed in is missing attribute: {repr(e)}"
                ) from e

    def _call(self, endpoint: list[str | int], params: dict[str, Any] = None) -> Any:
        if params is None:
            params = {}

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_params = self._create_cached_params(params)
        cache_key = f"{url}{cache_params}"
        cached_response = self._get_results_from_cache(cache_key)

        if cached_response is not None:
            return cached_response["results"]

        self._update_params(params)
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
        )

        data = response.json()

        if "message" in data:
            raise ApiError(data["message"])
        if data.get("code", 200) != 200:
            raise ApiError(data.get("status"))
        if "data" in data:
            data = data["data"]

        if response.status_code == 200:
            self._save_results_to_cache(cache_key, data)

        return data["results"]

    def comic(self, _id: int) -> Comic:
        """Request data for a comic based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The comic id.

        Returns
        -------
        Comic
            A :class:`Comic` object

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["comics", _id])[0]
            adapter = TypeAdapter(Comic)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def comic_characters(
        self, _id: int, params: dict[str, Any] | None = None
    ) -> list[Character]:
        """Request a list of characters from a comic.

        Parameters
        ----------
        _id: int
            The comic id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Character]
            A list of :class:`Character` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["comics", _id, "characters"], params=params)
            adapter = TypeAdapter(list[Character])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def comic_creators(self, _id: int, params: dict[str, Any] | None = None) -> list[Creator]:
        """Request a list of creators from a comic.

        Parameters
        ----------
        _id: int
            The comic id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Creator]
            A list of :class:`Creator` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["comics", _id, "creators"], params=params)
            adapter = TypeAdapter(list[Creator])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def comic_events(self, _id: int, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events from a comic.

        Parameters
        ----------
        _id: int
            The comic id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["comics", _id, "events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def comic_stories(self, _id: int, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories from a comic.

        Parameters
        ----------
        _id: int
            The comic id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["comics", _id, "stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def comics_list(self, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series(self, _id: int) -> Series:
        """Request data for a series based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The series id.

        Returns
        -------
        Series
            :class:`Series` object

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["series", _id])[0]
            adapter = TypeAdapter(Series)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_characters(
        self, _id: int, params: dict[str, Any] | None = None
    ) -> list[Character]:
        """Request a list of characters from a series.

        Parameters
        ----------
        _id: int
            The series id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Character]
            A list of :class:`Character` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series", _id, "characters"], params=params)
            adapter = TypeAdapter(list[Character])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_comics(self, _id: int, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics from a series.

        Parameters
        ----------
        _id: int
            The series id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series", _id, "comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_creators(self, _id: int, params: dict[str, Any] | None = None) -> list[Creator]:
        """Request a list of creators from a series.

        Parameters
        ----------
        _id: int
            The series id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Creator]
            A list of :class:`Creator` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series", _id, "creators"], params=params)
            adapter = TypeAdapter(list[Creator])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_events(self, _id: int, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events from a series.

        Parameters
        ----------
        _id: int
            The series id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series", _id, "events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_stories(self, _id: int, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories from a series.

        Parameters
        ----------
        _id: int
            The series id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series", _id, "stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def series_list(self, params: dict[str, Any] | None = None) -> list[Series]:
        """Request a list of series.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Series]
            A list of :class:`Series` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["series"], params=params)
            adapter = TypeAdapter(list[Series])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def creator(self, _id: int) -> Creator:
        """Request data for a creator based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The creator id.

        Returns
        -------
        Creator
            :class:`Creator` object

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["creators", _id])[0]
            adapter = TypeAdapter(Creator)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def creator_comics(self, _id: int, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics from a creator.

        Parameters
        ----------
        _id: int
            The creator id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["creators", _id, "comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def creator_events(self, _id: int, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events from a creator.

        Parameters
        ----------
        _id: int
            The creator id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["creators", _id, "events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def creator_series(self, _id: int, params: dict[str, Any] | None = None) -> list[Series]:
        """Request a list of series by a creator.

        Parameters
        ----------
        _id: int
            The creator id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Series]
            A list of :class:`Series` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["creators", _id, "series"], params=params)
            adapter = TypeAdapter(list[Series])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def creator_stories(self, _id: int, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories from a creator.

        Parameters
        ----------
        _id: int
            The creator id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["creators", _id, "stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def creators_list(self, params: dict[str, Any] | None = None) -> list[Creator]:
        """Request a list of creators.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Creator]
            A list of :class:`Creator` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["creators"], params=params)
            adapter = TypeAdapter(list[Creator])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def character(self, _id: int) -> Character:
        """Request data for a character based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The character id.

        Returns
        -------
        Character
            A :class:`Character` object.

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["characters", _id])[0]
            adapter = TypeAdapter(Character)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def character_comics(self, _id: int, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics for a character.

        Parameters
        ----------
        _id: int
            The character id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["characters", _id, "comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def character_events(self, _id: int, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events for a character.

        Parameters
        ----------
        _id: int
            The character id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["characters", _id, "events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def character_series(self, _id: int, params: dict[str, Any] | None = None) -> list[Series]:
        """Request a list of series for a character.

        Parameters
        ----------
        _id: int
            The character id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Series]
            A list of :class:`Series` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["characters", _id, "series"], params=params)
            adapter = TypeAdapter(list[Series])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def character_stories(self, _id: int, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories for a character.

        Parameters
        ----------
        _id: int
            The character id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["characters", _id, "stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def characters_list(self, params: dict[str, Any] | None = None) -> list[Character]:
        """Request a list of characters.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Character]
            A list of :class:`Character` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["characters"], params=params)
            adapter = TypeAdapter(list[Character])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def story(self, _id: int) -> Story:
        """Request data for a Story based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The story id.

        Returns
        -------
        Story
            A :class:`Story` object

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["stories", _id])[0]
            adapter = TypeAdapter(Story)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def story_characters(
        self, _id: int, params: dict[str, Any] | None = None
    ) -> list[Character]:
        """Request a list of characters from a story.

        Parameters
        ----------
        _id: int
            The story id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Character]
            A list of :class:`Character` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories", _id, "characters"], params=params)
            adapter = TypeAdapter(list[Character])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def story_comics(self, _id: int, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics for a story.

        Parameters
        ----------
        _id: int
            The story id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories", _id, "comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def story_creators(self, _id: int, params: dict[str, Any] | None = None) -> list[Creator]:
        """Request a list of creators from a story.

        Parameters
        ----------
        _id: int
            The story id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Creator]
            A list of :class:`Creator` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories", _id, "creators"], params=params)
            adapter = TypeAdapter(list[Creator])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def story_events(self, _id: int, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events for a story.

        Parameters
        ----------
        _id: int
            The story id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories", _id, "events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def story_series(self, _id: int, params: dict[str, Any] | None = None) -> list[Series]:
        """Request a list of series for a story.

        Parameters
        ----------
        _id: int
            The story id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Series]
            A list of :class:`Series` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories", _id, "series"], params=params)
            adapter = TypeAdapter(list[Series])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def stories_list(self, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def event(self, _id: int) -> Event:
        """Request data for an event based on it's ``_id``.

        Parameters
        ----------
        _id: int
            The event id.

        Returns
        -------
        Event
            A :class:`Event` object

        Raises
        ------
        ApiError
            If requested information is not valid.
        """
        try:
            result = self._call(["events", _id])[0]
            adapter = TypeAdapter(Event)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ApiError(err) from err

    def event_characters(
        self, _id: int, params: dict[str, Any] | None = None
    ) -> list[Character]:
        """Request a list of characters from an event.

        Parameters
        ----------
        _id: int
            The event id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Character]
            A list of :class:`Character` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events", _id, "characters"], params=params)
            adapter = TypeAdapter(list[Character])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def event_comics(self, _id: int, params: dict[str, Any] | None = None) -> list[Comic]:
        """Request a list of comics for an event.

        Parameters
        ----------
        _id: int
            The event id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Comic]
            A list of :class:`Comic` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events", _id, "comics"], params=params)
            adapter = TypeAdapter(list[Comic])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def event_creators(self, _id: int, params: dict[str, Any] | None = None) -> list[Creator]:
        """Request a list of creators from an event.

        Parameters
        ----------
        _id: int
            The event id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Creator]
            A list of :class:`Creator` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events", _id, "creators"], params=params)
            adapter = TypeAdapter(list[Creator])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def event_series(self, _id: int, params: dict[str, Any] | None = None) -> list[Series]:
        """Request a list of series for an event.

        Parameters
        ----------
        _id: int
            The event id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Series]
            A list of :class:`Series` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events", _id, "series"], params=params)
            adapter = TypeAdapter(list[Series])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def event_stories(self, _id: int, params: dict[str, Any] | None = None) -> list[Story]:
        """Request a list of stories for an event.

        Parameters
        ----------
        _id: int
            The event id.
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Story]
            A list of :class:`Story` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events", _id, "stories"], params=params)
            adapter = TypeAdapter(list[Story])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err

    def events_list(self, params: dict[str, Any] | None = None) -> list[Event]:
        """Request a list of events.

        Parameters
        ----------
        params: dict, optional
            Parameters to add to the request.

        Returns
        -------
        list[Event]
            A list of :class:`Event` objects.
        """
        if params is None:
            params = {}

        try:
            results = self._call(["events"], params=params)
            adapter = TypeAdapter(list[Event])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ApiError(err) from err
