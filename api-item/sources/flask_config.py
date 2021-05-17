class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clean_msa@postgres-item:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    API_ITEM = "http://api-item:5001"
    API_ALARM = "http://api-alarm:6001"
    API_USER = "http://api-user:7001"

    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_DB = 0

    INTERNAL_URLS = [
        "localhost:5001",
        "localhost:6001",
        "localhost:7001",
        "localhost",
        "api-user:7001",
        "api-item:5001",
        "api-alarm:6001"
    ]


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class QAConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clean_msa@localhost:35434/postgres'
    API_ITEM = "http://localhost:5001"
    API_ALARM = "http://localhost:6001"
    API_USER = "http://localhost:7001"
    REDIS_HOST = "localhost"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:clean_msa@localhost:35434/postgres'
    API_ITEM = "http://localhost:5001"
    API_ALARM = "http://localhost:6001"
    API_USER = "http://localhost:7001"
    REDIS_HOST = "localhost"
