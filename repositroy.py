from typing import Union, Optional
from abstracs import BaseInMemoryStore, Singleton
import threading
import time
import pickle
import os
from conf import PERSIST_DATA

__all__ = [
    'InMemoryRepository',
    'PersistDataRepository'
]

from custom_types import T


class InMemoryRepository(Singleton, BaseInMemoryStore):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()
        super().__init__()

    def set(self, key, value, ttl=None):
        print(key, value)
        with self.lock:
            data = {'value': value, 'expire_at': int(time.time()) + int(ttl) if ttl else None}
            if key in self.store:
                self.store[key].update(data)
            else:
                self.store[key] = data

    def get(self, key):
        with self.lock:
            if key in self.store:
                entry = self.store[key]
                if entry['expire_at'] is not None and int(time.time()) >= entry['expire_at']:
                    self.store.pop(key)
                    return None
                return entry['value']
            return None

    def delete(self, key):
        with self.lock:
            if key in self.store:
                self.store.pop(key)

    def expire(self, key: str, seconds: Union[str, int]):
        with self.lock:
            if key in self.store:
                self.store[key]['expire_at'] = int(time.time()) + int(seconds)

    def ttl(self, key):
        with self.lock:
            if key in self.store:
                entry = self.store[key]
                if entry['expire_at'] is not None:
                    return entry['expire_at'] - int(time.time())
                else:
                    return -1  # No expiration time set
            return -2  # Key does not exist


class PersistDataRepository(BaseInMemoryStore):
    def __init__(self, filename='store.pkl'):
        self.store = {}
        self.lock = threading.Lock()
        self.filename = filename
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.store = pickle.load(f)

    def _save_data(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.store, f)

    def set(self, key, value, ttl=None):
        with self.lock:
            data = {'value': value, 'expire_at': int(time.time()) + int(ttl) if ttl else None}
            if key in self.store:
                self.store[key].update(data)
                self._save_data()
            else:
                self.store[key] = data
                self._save_data()

    def get(self, key):
        with self.lock:
            if key in self.store:
                entry = self.store[key]
                if entry['expire_at'] is not None and int(time.time()) >= entry['expire_at']:
                    self.store.pop(key)
                    self._save_data()
                    return None
                return self.store[key]['value']
            return None

    def delete(self, key: str) -> None:
        with self.lock:
            if key in self.store:
                self.store.pop(key)
                self._save_data()

    def expire(self, key: str, seconds: Union[str, int]) -> None:
        with self.lock:
            if key in self.store:
                self.store[key]['expire_at'] = int(time.time()) + int(seconds)
                self._save_data()

    def ttl(self, key: str) -> int:
        with self.lock:
            if key in self.store:
                entry = self.store[key]
                if entry['expire_at'] is not None:
                    return entry['expire_at'] - int(time.time())
                else:
                    return -1  # No expiration time set
            return -2  # Key does not exist


class PyInMemStore(BaseInMemoryStore):

    def __init__(self):
        self.store = PersistDataRepository() if PERSIST_DATA else InMemoryRepository()

    def set(self, key: str, value: T, ttl: Union[str, int]=None) -> None:
        return self.store.set(key, value, ttl)

    def get(self, key: str) -> Optional[T]:
        return self.store.get(key)

    def expire(self, key: str, expire_time: str) -> None:
        return self.store.expire(key, expire_time)

    def ttl(self, key: str) -> int:
        return self.store.ttl(key)

    def delete(self, key: str) -> None:
        return self.store.delete(key)
