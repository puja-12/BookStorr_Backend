import json

import redis





class RedisFunction:
    redis_cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    @classmethod
    def extract(cls, key):
        return cls.redis_cache.get(key)

    @classmethod
    def save(cls, key, cache_data):
        return cls.redis_cache.set(key, json.dumps(cache_data))

    @classmethod
    def get_keys(cls):
        return cls.redis_cache.keys('*')
