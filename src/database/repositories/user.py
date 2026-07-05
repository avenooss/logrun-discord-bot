"""User repository for database operations."""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import DiscordUser
from src.utils.errors import DatabaseError

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for Discord user operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository.
        
        Args:
            session: AsyncSession instance
        """
        self.session = session

    async def get_user(self, discord_id: int) -> Optional[DiscordUser]:
        """Get user by Discord ID.
        
        Args:
            discord_id: Discord user ID
            
        Returns:
            DiscordUser instance or None
        """
        try:
            stmt = select(DiscordUser).where(DiscordUser.discord_id == discord_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            raise DatabaseError(f"Failed to retrieve user: {e}")

    async def create_user(
        self, discord_id: int, username: str, tag: str
    ) -> DiscordUser:
        """Create new Discord user.
        
        Args:
            discord_id: Discord user ID
            username: Discord username
            tag: Discord tag (username#xxxx)
            
        Returns:
            Created DiscordUser instance
        """
        try:
            user = DiscordUser(
                discord_id=discord_id, discord_username=username, discord_tag=tag
            )
            self.session.add(user)
            await self.session.flush()
            logger.info(f"Created user: {discord_id}")
            return user
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise DatabaseError(f"Failed to create user: {e}")

    async def update_user(self, discord_id: int, **kwargs) -> Optional[DiscordUser]:
        """Update Discord user.
        
        Args:
            discord_id: Discord user ID
            **kwargs: Fields to update
            
        Returns:
            Updated DiscordUser instance or None
        """
        try:
            user = await self.get_user(discord_id)
            if not user:
                return None

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await self.session.flush()
            logger.info(f"Updated user: {discord_id}")
            return user
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise DatabaseError(f"Failed to update user: {e}")

    async def mark_verified(self, discord_id: int) -> Optional[DiscordUser]:
        """Mark user as verified.
        
        Args:
            discord_id: Discord user ID
            
        Returns:
            Updated DiscordUser instance or None
        """
        return await self.update_user(discord_id, verified=1)

    async def delete_user(self, discord_id: int) -> bool:
        """Delete Discord user.
        
        Args:
            discord_id: Discord user ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            user = await self.get_user(discord_id)
            if not user:
                return False

            await self.session.delete(user)
            await self.session.flush()
            logger.info(f"Deleted user: {discord_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            raise DatabaseError(f"Failed to delete user: {e}")
