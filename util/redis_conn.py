import redis
from config import config


class RedisUtil:
    def __init__(self) -> None:
        pool = redis.ConnectionPool(**config.configs['redis_db'], decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

redisUtil = RedisUtil()

