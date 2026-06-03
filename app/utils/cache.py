"""
In-memory cache with TTL.

NOTE: Not shared across workers. Production was supposed to use Redis
(see config.REDIS_URL) but the Redis client integration is incomplete.
See integrations/redis_client.py for the half-finished version.
"""
import time
from threading import RLock


class TTLCache:
    def __init__(self, default_ttl=300):
        self._store = {}
        self._lock = RLock()
        self.default_ttl = default_ttl

    def get(self, key):
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key, value, ttl=None):
        with self._lock:
            ttl = ttl if ttl is not None else self.default_ttl
            self._store[key] = (value, time.time() + ttl)

    def invalidate(self, key):
        with self._lock:
            self._store.pop(key, None)

    def clear(self):
        with self._lock:
            self._store.clear()


_cache = TTLCache()


def get_cache():
    return _cache
