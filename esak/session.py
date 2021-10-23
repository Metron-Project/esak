import datetime
import hashlib
import platform
import urllib.parse
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

import requests
from marshmallow import ValidationError

from esak import __version__
from esak import character as ch
from esak import comic as com
from esak import creator as cr
from esak import event as ev
from esak import exceptions
from esak import series as ser
from esak import sqlite_cache, stories


class Session:
    def __init__(
        self,
        public_key: str,
        private_key: str,
        cache: Optional[sqlite_cache.SqliteCache] = None,
    ):

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

    def call(self, endpoint: List[Union[str, int]], params: Dict[str, Any] = None) -> Any:
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
        try:
            return com.ComicSchema().load(self.call(["comics", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def comics_list(self, params: Optional[Dict[str, Any]] = None) -> com.ComicsList:
        if params is None:
            params = {}

        return com.ComicsList(self.call(["comics"], params=params))

    def series(self, _id: int) -> ser.Series:
        try:
            return ser.SeriesSchema().load(self.call(["series", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def series_list(self, params: Optional[Dict[str, Any]] = None) -> ser.SeriesList:
        if params is None:
            params = {}

        return ser.SeriesList(self.call(["series"], params=params))

    def creator(self, _id: int) -> cr.Creator:
        try:
            return cr.CreatorsSchema().load(self.call(["creators", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def creators_list(self, params: Optional[Dict[str, Any]] = None) -> cr.CreatorsList:
        if params is None:
            params = {}

        return cr.CreatorsList(self.call(["creators"], params=params))

    def character(self, _id: int) -> ch.Character:
        try:
            return ch.CharacterSchema().load(self.call(["characters", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def characters_list(self, params: Optional[Dict[str, Any]] = None) -> ch.CharactersList:
        if params is None:
            params = {}

        return ch.CharactersList(self.call(["characters"], params=params))

    def story(self, _id: int) -> stories.Stories:
        try:
            return stories.StoriesSchema().load(self.call(["stories", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def stories_list(self, params: Optional[Dict[str, Any]] = None) -> stories.StoriesList:
        if params is None:
            params = {}

        return stories.StoriesList(self.call(["stories"], params=params))

    def event(self, _id: int) -> ev.Events:
        try:
            return ev.EventSchema().load(self.call(["events", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def events_list(self, params: Optional[Dict[str, Any]] = None) -> ev.EventsList:
        if params is None:
            params = {}

        return ev.EventsList(self.call(["events"], params=params))
