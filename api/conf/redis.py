import redis

redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)


def redis_connection():
    return redis_client
