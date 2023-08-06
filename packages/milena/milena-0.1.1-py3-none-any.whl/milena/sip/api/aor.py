from __future__ import annotations

from typing import Optional, Dict
from functools import lru_cache

from ..tools import parse_aor, stringify_aor
from ...abc import Protocol


class AOR(Protocol):
    def __init__(
        self, string: Optional[str] = None, dictionary: Dict[str, str] = None
    ) -> None:
        if not string and not dictionary:
            raise ValueError("You need to enter a valid dictionary or a string AOR")

        if dictionary and not "uri" in dictionary:
            raise ValueError("Invalid sip AOR format")

        self._string = string
        self._dictionary = dictionary

    @lru_cache(maxsize=None)
    def dict(self) -> Dict[str, Optional[str]]:
        if not self._dictionary:
            self._dictionary = parse_aor(self._string)

        return self._dictionary

    @lru_cache(maxsize=None)
    def string(self) -> str:
        if not self._string:
            self._string = stringify_aor(self._dictionary)

        return self._string
