from typing import TypeVar, TypedDict, Optional

__all__ = [
    'T',
    'InMemoryDataType'
]

T = TypeVar('T')


class InMemoryDataType(TypedDict):
    name: str
    value: T
    expire_time: Optional[str]
