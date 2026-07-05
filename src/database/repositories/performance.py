"""Performance repository for database operations."""

import logging
from typing import List, Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Performance
from src.utils.errors import DatabaseError

logger = logging.getLogger(__name__)


class PerformanceRepository:
    """Repository for performance data operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository.
        
        Args:
            session: AsyncSession instance
        """
        self.session = session

    async def get_performance(self, performance_id: int) -> Optional[Performance]:
        """Get performance record by ID.
        
        Args:
            performance_id: Performance record ID
            
        Returns:
            Performance instance or None
        """
        try:
            stmt = select(Performance).where(Performance.id == performance_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get performance: {e}")
            raise DatabaseError(f"Failed to retrieve performance: {e}")

    async def get_character_performance(
        self, character_id: int
    ) -> Optional[Performance]:
        """Get performance data for character.
        
        Args:
            character_id: Character database ID
            
        Returns:
            Performance instance or None
        """
        try:
            stmt = select(Performance).where(Performance.character_id == character_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get character performance: {e}")
            raise DatabaseError(f"Failed to retrieve performance: {e}")

    async def create_performance(
        self,
        character_id: int,
        discord_id: int,
        heroic_best_perf_avg: float = 0.0,
    ) -> Performance:
        """Create new performance record.
        
        Args:
            character_id: Character database ID
            discord_id: Discord user ID
            heroic_best_perf_avg: Heroic best performance average
            
        Returns:
            Created Performance instance
        """
        try:
            performance = Performance(
                character_id=character_id,
                discord_id=discord_id,
                heroic_best_perf_avg=heroic_best_perf_avg,
            )
            self.session.add(performance)
            await self.session.flush()
            logger.info(f"Created performance record for character: {character_id}")
            return performance
        except Exception as e:
            logger.error(f"Failed to create performance: {e}")
            raise DatabaseError(f"Failed to create performance: {e}")

    async def update_performance(
        self, performance_id: int, **kwargs
    ) -> Optional[Performance]:
        """Update performance record.
        
        Args:
            performance_id: Performance record ID
            **kwargs: Fields to update
            
        Returns:
            Updated Performance instance or None
        """
        try:
            performance = await self.get_performance(performance_id)
            if not performance:
                return None

            for key, value in kwargs.items():
                if hasattr(performance, key):
                    setattr(performance, key, value)

            await self.session.flush()
            logger.info(f"Updated performance: {performance_id}")
            return performance
        except Exception as e:
            logger.error(f"Failed to update performance: {e}")
            raise DatabaseError(f"Failed to update performance: {e}")

    async def get_leaderboard(
        self, discord_id: int, limit: int = 10
    ) -> List[Performance]:
        """Get top performers.
        
        Args:
            discord_id: Discord guild ID (for context)
            limit: Number of results to return
            
        Returns:
            List of Performance instances sorted by performance
        """
        try:
            stmt = (
                select(Performance)
                .where(Performance.discord_id == discord_id)
                .order_by(desc(Performance.heroic_best_perf_avg))
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            raise DatabaseError(f"Failed to retrieve leaderboard: {e}")
