from ...abc import Protocol


from typing import Optional, Dict
from functools import lru_cache

from ..tools import (
    is_valid_auth_info_header,
    parse_authentication_info_header,
    stringify_auth_header,
)


class AuthenticationInfo(Protocol):
    def __init__(
        self, string: Optional[str] = None, dictionary: Dict[str, str] = None
    ) -> None:
        if not string and not dictionary:
            raise ValueError("You need to enter a valid dictionary or a string")

        if string and not is_valid_auth_info_header(string):
            raise ValueError("Invalid sip authentication info header format")

        self._string = string
        self._dictionary = dictionary

    @lru_cache(maxsize=None)
    def dict(self) -> Dict[str, Optional[str]]:
        if not self._dictionary:
            self._dictionary = parse_authentication_info_header(self._string)

        return self._dictionary

    @lru_cache(maxsize=None)
    def string(self) -> str:
        if not self._string:
            self._string = stringify_auth_header(self._dictionary)

        return self._string

    def __str__(self) -> str:
        if not self._string:
            self._string = stringify_auth_header(self._dictionary)

        return f"Authentication-Info: {self._string}"
