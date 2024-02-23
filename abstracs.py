from abc import ABC, abstractmethod
import abc
from typing import Union, Optional
from custom_types import T

__all__ = [
    'Singleton',
    'BaseInMemoryStore'
]


class BaseInMemoryStore(ABC):

    @abstractmethod
    def set(self, key: str, value: T, ttl: Union[str, int]) -> None:
        raise NotImplementedError("Method Set Is Not Implemented !")

    @abstractmethod
    def get(self, key: str) -> Optional[T]:
        raise NotImplementedError("Method Get Is Not Implemented !")

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError("Method Delete Is Not Implemented !")

    @abstractmethod
    def expire(self, key: str, expire_time: str) -> None:
        raise NotImplementedError("Method Delete Is Not Implemented !")

    @abstractmethod
    def ttl(self, key: str) -> int:
        raise NotImplementedError("Method Ttl Is Not Implemented !")


class Singleton(abc.ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        _instance = None
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance
