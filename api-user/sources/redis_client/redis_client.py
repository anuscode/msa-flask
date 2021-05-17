import redis
from flask import current_app as app
from shared.annotations import skippable


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisPoolManager(metaclass=Singleton):

    def __init__(self):
        host = app.config["REDIS_HOST"]
        port = app.config["REDIS_PORT"]
        db = app.config["REDIS_DB"]
        self._connection_pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)

    @property
    def connection_pool(self):
        return self._connection_pool

    @connection_pool.setter
    def connection_pool(self):
        raise Exception("do not touch it..")


class RedisClient:
    pool_manager = None

    def __init__(self):
        raise Exception("Please do not initiate it..")

    @classmethod
    def connect(cls):
        if not cls.pool_manager:
            cls.pool_manager = RedisPoolManager()
        connection_pool = cls.pool_manager.connection_pool
        return redis.StrictRedis(connection_pool=connection_pool, charset="utf-8")

    @classmethod
    def execute(cls, *args, **kwargs):
        redis_connection = cls.connect()
        return redis_connection.execute_command(*args, **kwargs)

    @classmethod
    @skippable(None)
    def set(cls, name, value, ex=None):
        con = cls.connect()
        con.set(name, value, ex=ex)

    @classmethod
    @skippable(None)
    def get(cls, name):
        con = cls.connect()
        value = con.get(name)
        return value

    @classmethod
    @skippable([])
    def zrange(cls, name, start, end, desc=False, withscores=False, score_cast_func=float):
        con = cls.connect()
        value = con.zrange(name, start, end, desc=desc, withscores=withscores, score_cast_func=score_cast_func)
        return value
