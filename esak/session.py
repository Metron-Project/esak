import datetime
import hashlib
import urllib.parse
from collections import OrderedDict
from typing import Any, Dict, Optional

import requests
from marshmallow import ValidationError

from esak import (
    character,
    characters_list,
    comic,
    comics_list,
    creator,
    creators_list,
    exceptions,
    series,
    series_list,
)


class Session:
    api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def __init__(self, public_key, private_key, cache=None):

        self.public_key = public_key
        self.private_key = private_key
        self.cache = cache

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

    def call(self, endpoint, params=None):
        if params is None:
            params = {}

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_params = self._create_cached_params(params)
        cache_key = f"{url}{cache_params}"
        cached_response = self._get_results_from_cache(cache_key)

        if cached_response is not None:
            return cached_response

        self._update_params(params)
        response = requests.get(url, params=params)

        data = response.json()

        if "message" in data:
            raise exceptions.ApiError(data["message"])

        if response.status_code == 200:
            self._save_results_to_cache(cache_key, data)

        return data

    def comic(self, _id: int) -> comic.Comic:
        try:
            return comic.ComicSchema().load(self.call(["comics", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def comics_list(self, params: Optional[Dict[str, Any]] = None) -> comics_list.ComicsList:
        if params is None:
            params = {}

        return comics_list.ComicsList(self.call(["comics"], params=params))

    def series(self, _id=None, params=None):
        result = None
        if _id:
            try:
                result = series.SeriesSchema().load(self.call(["series", _id]))
                result.session = self
            except ValidationError as error:
                raise exceptions.ApiError(error)
        elif params:
            try:
                api_call = self.call(["series"], params)

                if api_call.get("code", 200) != 200:
                    raise exceptions.ApiError(api_call.get("status"))

                result = series.SeriesSchema().load(
                    api_call.get("data", {}).get("results"), many=True
                )
                for r in result:
                    r.session = self
            except ValidationError as error:
                raise exceptions.ApiError(error)

        return result

    def series_list(self, params=None):
        if params is None:
            params = {}

        return series_list.SeriesList(self.call(["series"], params=params))

    def creator(self, _id):
        try:
            return creator.CreatorsSchema().load(self.call(["creators", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def creators_list(self, params=None):
        if params is None:
            params = {}

        return creators_list.CreatorsList(self.call(["creators"], params=params))

    def character(self, _id):
        try:
            return character.CharactersSchema().load(self.call(["characters", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

    def characters_list(self, params=None):
        if params is None:
            params = {}

        return characters_list.CharactersList(self.call(["characters"], params=params))
