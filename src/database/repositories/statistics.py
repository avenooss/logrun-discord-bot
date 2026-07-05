"""Statistics repository for database operations."""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import GuildStatistics
from src.utils.errors import DatabaseError

logger = logging.getLogger(__name__)


class StatisticsRepository:
    """Repository for guild statistics operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository.
        
        Args:
            session: AsyncSession instance
        """
        self.session = session

    async def get_guild_stats(self, guild_id: int) -> Optional[GuildStatistics]:
        """Get guild statistics.
        
        Args:
            guild_id: Guild database ID
            
        Returns:
            GuildStatistics instance or None
        """
        try:
            stmt = select(GuildStatistics).where(GuildStatistics.guild_id == guild_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get guild stats: {e}")
            raise DatabaseError(f"Failed to retrieve guild statistics: {e}")

    async def create_guild_stats(self, guild_id: int) -> GuildStatistics:
        """Create new guild statistics record.
        
        Args:
            guild_id: Guild database ID
            
        Returns:
            Created GuildStatistics instance
        """
        try:
            stats = GuildStatistics(guild_id=guild_id)
            self.session.add(stats)
            await self.session.flush()
            logger.info(f"Created guild stats for: {guild_id}")
            return stats
        except Exception as e:
            logger.error(f"Failed to create guild stats: {e}")
            raise DatabaseError(f"Failed to create guild statistics: {e}")

    async def update_guild_stats(
        self, guild_id: int, **kwargs
    ) -> Optional[GuildStatistics]:
        """Update guild statistics.
        
        Args:
            guild_id: Guild database ID
            **kwargs: Fields to update
            
        Returns:
            Updated GuildStatistics instance or None
        """
        try:
            stats = await self.get_guild_stats(guild_id)
            if not stats:
                stats = await self.create_guild_stats(guild_id)

            for key, value in kwargs.items():
                if hasattr(stats, key):
                    setattr(stats, key, value)

            await self.session.flush()
            logger.info(f"Updated guild stats: {guild_id}")
            return stats
        except Exception as e:
            logger.error(f"Failed to update guild stats: {e}")
            raise DatabaseError(f"Failed to update guild statistics: {e}")
