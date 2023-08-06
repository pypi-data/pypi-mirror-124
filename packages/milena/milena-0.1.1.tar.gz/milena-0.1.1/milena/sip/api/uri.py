from __future__ import annotations

from functools import lru_cache
from typing import Optional

from ..tools import stringify_uri, is_valid_uri, parse_uri, DictUri
from ...abc import Protocol


class URI(Protocol):
    def __init__(
        self, string: Optional[str] = None, dictionary: DictUri = None
    ) -> None:
        if not string and not dictionary:
            raise ValueError("You need to enter a valid dictionary or a string sip URI")

        if string and not is_valid_uri(string):
            raise ValueError("Invalid sip URI format")

        if dictionary and not "host" in dictionary:
            raise ValueError("Invalid sip URI format")

        self._string = string
        self._dictionary = dictionary

    @lru_cache(maxsize=None)
    def string(self) -> str:
        if not self._string:
            self._string = stringify_uri(self._dictionary)

        return self._string

    @lru_cache(maxsize=None)
    def dict(self) -> DictUri:
        if not self._dictionary:
            self._dictionary = parse_uri(self._string)

        return self._dictionary
