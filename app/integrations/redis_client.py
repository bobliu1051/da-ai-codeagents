"""
Redis client wrapper.

NOTE: This module is INCOMPLETE. The intent was to swap the in-memory cache
in utils/cache.py for Redis. Most of the code is stubbed. Don't use yet.
"""
# import redis  # uncomment when you actually install redis


class RedisCache:
    def __init__(self, url):
        self.url = url
        # self.client = redis.from_url(url)
        raise NotImplementedError("redis backend not finished")

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, ttl=None):
        raise NotImplementedError
