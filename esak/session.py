"""
Session module.

This module provides the following classes:

- Session
"""
import datetime
import hashlib
import platform
import urllib.parse
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

import requests
from marshmallow import ValidationError

# Alias these modules to prevent namespace collision with methods.
from esak import __version__
from esak import character as ch
from esak import comic as com
from esak import creator as cr
from esak import event as ev
from esak import exceptions
from esak import series as ser
from esak import sqlite_cache, stories


class Session:
    """
    Session to request api endpoints.

    :param str public_key: The public_key for authentication with Marvel
    :param str private_key: The private_key used for authentication with Marvel
    :param SqliteCache optional: SqliteCache to use
    """

    def __init__(
        self,
        public_key: str,
        private_key: str,
        cache: Optional[sqlite_cache.SqliteCache] = None,
    ):
        """Intialize a new Session."""
        self.public_key = public_key
        self.private_key = private_key
        self.cache = cache
        self.api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def _create_cached_params(self, params: Dict[str, Any]) -> str:
        # Generate part of cache key before hash, apikey and timestamp added
        cache_params = ""
        if params:
            orderedParams = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
            cache_params = f"?{urllib.parse.urlencode(orderedParams)}"
        return cache_params

    def _create_auth_hash(self, now_string: str) -> str:
        auth_hash = hashlib.md5()
        auth_hash.update(now_string.encode("utf-8"))
        auth_hash.update(self.private_key.encode("utf-8"))
        auth_hash.update(self.public_key.encode("utf-8"))
        return auth_hash.hexdigest()

    def _update_params(self, params: Dict[str, Any]) -> None:
        now_string = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")

        params["hash"] = self._create_auth_hash(now_string)
        params["apikey"] = self.public_key
        params["ts"] = now_string

    def _get_results_from_cache(self, key: str) -> Optional[Any]:
        cached_response = None

        if self.cache:
            try:
                cached_response = self.cache.get(key)
                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise exceptions.CacheError(
                    f"Cache object passed in is missing attribute: {repr(e)}"
                )

        return cached_response

    def _save_results_to_cache(self, key: str, data: str) -> None:
        if self.cache:
            try:
                self.cache.store(key, data)
            except AttributeError as e:
                raise exceptions.CacheError(
                    f"Cache object passed in is missing attribute: {repr(e)}"
                )

    def _call(self, endpoint: List[Union[str, int]], params: Dict[str, Any] = None) -> Any:
        if params is None:
            params = {}

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_params = self._create_cached_params(params)
        cache_key = f"{url}{cache_params}"
        cached_response = self._get_results_from_cache(cache_key)

        if cached_response is not None:
            return cached_response

        header = {
            "User-Agent": f"esak/{__version__} ({platform.system()}; {platform.release()})"
        }
        self._update_params(params)
        response = requests.get(
            url,
            params=params,
            headers=header,
        )

        data = response.json()

        if "message" in data:
            raise exceptions.ApiError(data["message"])

        if response.status_code == 200:
            self._save_results_to_cache(cache_key, data)

        return data

    def comic(self, _id: int) -> com.Comic:
        """
        Request data for a comic based on it's ``_id``.

        :param int _id: The comic id.

        :return: :class:`Comic` object
        :rtype: Comic

        :raises: :class:`ApiError`
        """
        try:
            return com.ComicSchema().load(self._call(["comics", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def comic_characters(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ch.CharactersList:
        """
        Request a list of characters from a comic.

        :param int _id: The comic id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Character` objects.
        :rtype: CharactersList
        """
        if params is None:
            params = {}

        return ch.CharactersList(self._call(["comics", _id, "characters"], params=params))

    def comic_creators(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> cr.CreatorsList:
        """
        Request a list of creators from a comic.

        :param int _id: The comic id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Creator` objects.
        :rtype: CreatorsList
        """
        if params is None:
            params = {}

        return cr.CreatorsList(self._call(["comics", _id, "creators"], params=params))

    def comic_events(self, _id: int, params: Optional[Dict[str, Any]] = None) -> ev.EventsList:
        """
        Request a list of events from a comic.

        :param int _id: The comic id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Event` objects.
        :rtype: EventsList
        """
        if params is None:
            params = {}

        return ev.EventsList(self._call(["comics", _id, "events"], params=params))

    def comic_stories(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> stories.StoriesList:
        """
        Request a list of stories from a comic.

        :param int _id: The comic id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Stories` objects.
        :rtype: StoriesList
        """
        if params is None:
            params = {}

        return stories.StoriesList(self._call(["comics", _id, "stories"], params=params))

    def comics_list(self, params: Optional[Dict[str, Any]] = None) -> com.ComicsList:
        """
        Request a list of comics.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Comic` objects.
        :rtype: ComicsList
        """
        if params is None:
            params = {}

        return com.ComicsList(self._call(["comics"], params=params))

    def series(self, _id: int) -> ser.Series:
        """
        Request data for a series based on it's ``_id``.

        :param int _id: The series id.

        :return: :class:`Series` object
        :rtype: Series

        :raises: :class:`ApiError`
        """
        try:
            return ser.SeriesSchema().load(self._call(["series", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def series_characters(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ch.CharactersList:
        """
        Request a list of characters from a series.

        :param int _id: The series id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Character` objects.
        :rtype: CharactersList
        """
        if params is None:
            params = {}

        return ch.CharactersList(self._call(["series", _id, "characters"], params=params))

    def series_comics(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> com.ComicsList:
        """
        Request a list of comics from a series.

        :param int _id: The series id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Comic` objects.
        :rtype: ComicsList
        """
        if params is None:
            params = {}

        return com.ComicsList(self._call(["series", _id, "comics"], params=params))

    def series_creators(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> cr.CreatorsList:
        """
        Request a list of creators from a series.

        :param int _id: The series id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Creator` objects.
        :rtype: CreatorsList
        """
        if params is None:
            params = {}

        return cr.CreatorsList(self._call(["series", _id, "creators"], params=params))

    def series_events(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ev.EventsList:
        """
        Request a list of events from a series.

        :param int _id: The series id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Event` objects.
        :rtype: EventsList
        """
        if params is None:
            params = {}

        return ev.EventsList(self._call(["series", _id, "events"], params=params))

    def series_stories(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> stories.StoriesList:
        """
        Request a list of stories from a series.

        :param int _id: The series id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Stories` objects.
        :rtype: StoriesList
        """
        if params is None:
            params = {}

        return stories.StoriesList(self._call(["series", _id, "stories"], params=params))

    def series_list(self, params: Optional[Dict[str, Any]] = None) -> ser.SeriesList:
        """
        Request a list of series.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Series` objects.
        :rtype: SeriesList
        """
        if params is None:
            params = {}

        return ser.SeriesList(self._call(["series"], params=params))

    def creator(self, _id: int) -> cr.Creator:
        """
        Request data for a creator based on it's ``_id``.

        :param int _id: The creator id.

        :return: :class:`Creator` object
        :rtype: Creator

        :raises: :class:`ApiError`
        """
        try:
            return cr.CreatorsSchema().load(self._call(["creators", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def creator_comics(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> com.ComicsList:
        """
        Request a list of comics from a creator.

        :param int _id: The creator id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Comic` objects.
        :rtype: ComicsList
        """
        if params is None:
            params = {}

        return com.ComicsList(self._call(["creators", _id, "comics"], params=params))

    def creator_events(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ev.EventsList:
        """
        Request a list of events from a creator.

        :param int _id: The creator id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Event` objects.
        :rtype: EventsList
        """
        if params is None:
            params = {}

        return ev.EventsList(self._call(["creators", _id, "events"], params=params))

    def creator_series(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ser.SeriesList:
        """
        Request a list of series by a creator.

        :param int _id: The creator id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Series` objects.
        :rtype: SeriesList
        """
        if params is None:
            params = {}

        return ser.SeriesList(self._call(["creators", _id, "series"], params=params))

    def creator_stories(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> stories.StoriesList:
        """
        Request a list of stories from a creator.

        :param int _id: The creator id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Stories` objects.
        :rtype: StoriesList
        """
        if params is None:
            params = {}

        return stories.StoriesList(self._call(["creators", _id, "stories"], params=params))

    def creators_list(self, params: Optional[Dict[str, Any]] = None) -> cr.CreatorsList:
        """
        Request a list of creators.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Creator` objects.
        :rtype: CreatorsList
        """
        if params is None:
            params = {}

        return cr.CreatorsList(self._call(["creators"], params=params))

    def character(self, _id: int) -> ch.Character:
        """
        Request data for a character based on it's ``_id``.

        :param int _id: The character id.

        :return: :class:`Character` object
        :rtype: Character

        :raises: :class:`ApiError`
        """
        try:
            return ch.CharacterSchema().load(self._call(["characters", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def character_comics(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> com.ComicsList:
        """
        Request a list of comics for a character.

        :param int _id: The character id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Comic` objects.
        :rtype: ComicsList
        """
        if params is None:
            params = {}

        return com.ComicsList(self._call(["characters", _id, "comics"], params=params))

    def character_events(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ev.EventsList:
        """
        Request a list of events for a character.

        :param int _id: The character id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Event` objects.
        :rtype: EventsList
        """
        if params is None:
            params = {}

        return ev.EventsList(self._call(["characters", _id, "events"], params=params))

    def character_series(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> ser.SeriesList:
        """
        Request a list of series for a character.

        :param int _id: The character id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Series` objects.
        :rtype: SeriesList
        """
        if params is None:
            params = {}

        return ser.SeriesList(self._call(["characters", _id, "series"], params=params))

    def character_stories(
        self, _id: int, params: Optional[Dict[str, Any]] = None
    ) -> stories.StoriesList:
        """
        Request a list of stories for a character.

        :param int _id: The character id.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Stories` objects.
        :rtype: StoriesList
        """
        if params is None:
            params = {}

        return stories.StoriesList(self._call(["characters", _id, "stories"], params=params))

    def characters_list(self, params: Optional[Dict[str, Any]] = None) -> ch.CharactersList:
        """
        Request a list of characters.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Character` objects.
        :rtype: CharactersList
        """
        if params is None:
            params = {}

        return ch.CharactersList(self._call(["characters"], params=params))

    def story(self, _id: int) -> stories.Stories:
        """
        Request data for a Story based on it's ``_id``.

        :param int _id: The story id.

        :return: :class:`Stories` object
        :rtype: Stories

        :raises: :class:`ApiError`
        """
        try:
            return stories.StoriesSchema().load(self._call(["stories", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def stories_list(self, params: Optional[Dict[str, Any]] = None) -> stories.StoriesList:
        """
        Request a list of stories.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Stories` objects.
        :rtype: StoriesList
        """
        if params is None:
            params = {}

        return stories.StoriesList(self._call(["stories"], params=params))

    def event(self, _id: int) -> ev.Events:
        """
        Request data for an event based on it's ``_id``.

        :param int _id: The event id.

        :return: :class:`Event` object
        :rtype: Event

        :raises: :class:`ApiError`
        """
        try:
            return ev.EventSchema().load(self._call(["events", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def events_list(self, params: Optional[Dict[str, Any]] = None) -> ev.EventsList:
        """
        Request a list of events.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Event` objects.
        :rtype: EventsList
        """
        if params is None:
            params = {}

        return ev.EventsList(self._call(["events"], params=params))
