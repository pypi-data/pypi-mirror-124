from __future__ import annotations

from typing import Optional, Dict, Union
from functools import lru_cache

from ..tools import stringify_cseq_header, parse_cseq_header, is_valid_cseq_header
from ...abc import Protocol


class CSeq(Protocol):
    def __init__(
        self, string: Optional[str] = None, dictionary: Dict[str, str] = None
    ) -> None:
        if not string and not dictionary:
            raise ValueError("You need to enter a valid dictionary or a string")

        if string and not is_valid_cseq_header(string):
            raise ValueError("Invalid sip CSeq header format")

        self._string = string
        self._dictionary = dictionary

    @lru_cache(maxsize=None)
    def dict(self) -> Dict[str, Optional[str]]:
        if not self._dictionary:
            self._dictionary = parse_cseq_header(self._string)

        return self._dictionary

    @lru_cache(maxsize=None)
    def string(self) -> str:
        if not self._string:
            self._string = stringify_cseq_header(self._dictionary)

        return self._string

    def __str__(self) -> str:
        if not self._string:
            self._string = stringify_cseq_header(self._dictionary)

        return f"CSeq: {self._string}"
