"""
cache_service.py — Redis cache wrapper

Requires Redis running locally:
  redis-server          # mac/linux

Keys used by this project:
  explain:{word}        → Ollama-generated explanation  (TTL: 7 days)

The cache is optional — if Redis is unreachable every call falls through to
Ollama and the app still works. This is logged as a warning, not an error.
"""

import redis
import logging

logger = logging.getLogger(__name__)

# TTLs in seconds
TTL_EXPLANATION = 60 * 60 * 24 * 7   # 7 days — explanations don't change

_client: redis.Redis | None = None


def _get_client() -> redis.Redis | None:
    """
    Lazy-initialise the Redis client.
    Returns None (gracefully) if Redis is not reachable.
    """
    global _client
    if _client is not None:
        return _client
    try:
        client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        client.ping()          # will raise if Redis is down
        _client = client
        logger.info("Redis connected.")
        return _client
    except redis.ConnectionError:
        logger.warning("Redis not reachable — caching disabled.")
        return None


def cache_get(key: str) -> str | None:
    """Return cached string value, or None on miss / Redis unavailable."""
    client = _get_client()
    if client is None:
        return None
    try:
        return client.get(key)
    except Exception as e:
        logger.warning(f"Redis GET failed: {e}")
        return None


def cache_set(key: str, value: str, ttl: int = TTL_EXPLANATION) -> None:
    """Store a string value with a TTL. Silently skips if Redis unavailable."""
    client = _get_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, value)
    except Exception as e:
        logger.warning(f"Redis SET failed: {e}")