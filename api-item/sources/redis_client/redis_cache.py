import json

from redis_client.redis_client import RedisClient


def cache_v(ttl=600, prefix=""):
    """Memoize for any value type like string or integer.."""

    def decorator(f):
        def wrapper(*args, redis_key=None, **kwargs) -> dict:
            if not redis_key:
                if not args:
                    message = "redis_key is required value for cache annotation.."
                    raise ValueError(message)
                redis_key = args[0]
            redis_key = f"{prefix}{redis_key}"

            value = RedisClient.get(redis_key)

            if value:
                return value

            value = f(*args, **kwargs)
            RedisClient.set(redis_key, value, ex=ttl)
            return value

        return wrapper

    return decorator


def cache_r(ttl=600, prefix=""):
    """Memoize for any value type like array or dict.."""

    def decorator(f):
        def wrapper(*args, redis_key=None, **kwargs) -> dict:
            if not redis_key:
                if not args:
                    message = "redis_key is required value for cache annotation.."
                    raise ValueError(message)
                redis_key = args[0]
            redis_key = f"{prefix}{redis_key}"

            value = RedisClient.get(redis_key)

            if value:
                return json.loads(value)
            else:
                value = f(*args, **kwargs)
                dumped = json.dumps(value)
                RedisClient.set(redis_key, dumped, ex=ttl)
            return value

        return wrapper

    return decorator
