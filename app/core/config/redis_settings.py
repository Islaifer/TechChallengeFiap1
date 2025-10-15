from app.core.config import setting
import redis.asyncio as redis

RedisConnection = redis.from_url(setting.REDIS_URL, decode_responses=True)