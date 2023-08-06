from __future__ import annotations

from abc import ABC, abstractmethod, abstractclassmethod
from typing import Dict, Any, Union


class Protocol(ABC):
    @abstractmethod
    def string(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def _from_string(cls, content: str) -> Protocol:
        return cls(string=content)

    @classmethod
    def _from_dict(cls, content: Dict[str, str]) -> Protocol:
        return cls(dictionary=content)

    @classmethod
    def setup(
        cls, source: "string" | "dict", content: Union[str, Dict[str, Any]]
    ) -> Protocol:
        if source == "string":
            return cls._from_string(content=content)
        elif source == "dict":
            return cls._from_dict(content=content)
        else:
            raise RuntimeError("Invalid source format")

    def __str__(self) -> str:
        return self.string()
