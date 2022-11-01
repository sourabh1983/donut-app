import redis

redis_client = redis.StrictRedis(host="redis")


def publish_message(channel, message):
    redis_client.publish(channel, message)
