"""Cache management service."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple in-memory cache with TTL support."""

    def __init__(self, default_ttl: int = 1800):
        """Initialize cache manager.
        
        Args:
            default_ttl: Default time-to-live in seconds
        """
        self.cache: dict[str, tuple[Any, datetime]] = {}
        self.default_ttl = default_ttl

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        ttl = ttl or self.default_ttl
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
        self.cache[key] = (value, expires_at)
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")

    def get(self, key: str) -> Optional[Any]:
        """Get cache value.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None

        value, expires_at = self.cache[key]
        if datetime.now(timezone.utc) > expires_at:
            del self.cache[key]
            logger.debug(f"Cache expired: {key}")
            return None

        logger.debug(f"Cache hit: {key}")
        return value

    def delete(self, key: str) -> bool:
        """Delete cache value.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache deleted: {key}")
            return True
        return False

    def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()
        logger.info("Cache cleared")

    def cleanup_expired(self) -> int:
        """Remove expired entries.
        
        Returns:
            Number of entries removed
        """
        now = datetime.now(timezone.utc)
        expired_keys = [
            key for key, (_, expires_at) in self.cache.items() if now > expires_at
        ]

        for key in expired_keys:
            del self.cache[key]

        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")

        return len(expired_keys)
