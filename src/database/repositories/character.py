"""Character repository for database operations."""

import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Character
from src.utils.errors import DatabaseError

logger = logging.getLogger(__name__)


class CharacterRepository:
    """Repository for WoW character operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository.
        
        Args:
            session: AsyncSession instance
        """
        self.session = session

    async def get_character(self, character_id: int) -> Optional[Character]:
        """Get character by ID.
        
        Args:
            character_id: Character database ID
            
        Returns:
            Character instance or None
        """
        try:
            stmt = select(Character).where(Character.id == character_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get character: {e}")
            raise DatabaseError(f"Failed to retrieve character: {e}")

    async def get_character_by_name(
        self, name: str, realm: str, region: str
    ) -> Optional[Character]:
        """Get character by name, realm, and region.
        
        Args:
            name: Character name
            realm: Realm name
            region: Region code
            
        Returns:
            Character instance or None
        """
        try:
            stmt = select(Character).where(
                (Character.character_name == name)
                & (Character.realm == realm)
                & (Character.region == region)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Failed to get character by name: {e}")
            raise DatabaseError(f"Failed to retrieve character: {e}")

    async def get_user_characters(self, discord_id: int) -> List[Character]:
        """Get all characters for a Discord user.
        
        Args:
            discord_id: Discord user ID
            
        Returns:
            List of Character instances
        """
        try:
            stmt = select(Character).where(Character.discord_id == discord_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get user characters: {e}")
            raise DatabaseError(f"Failed to retrieve characters: {e}")

    async def create_character(
        self,
        discord_id: int,
        name: str,
        realm: str,
        region: str,
        guild: Optional[str] = None,
        class_name: Optional[str] = None,
        spec: Optional[str] = None,
    ) -> Character:
        """Create new character.
        
        Args:
            discord_id: Discord user ID
            name: Character name
            realm: Realm name
            region: Region code
            guild: Guild name (optional)
            class_name: Character class (optional)
            spec: Character specialization (optional)
            
        Returns:
            Created Character instance
        """
        try:
            character = Character(
                discord_id=discord_id,
                character_name=name,
                realm=realm,
                region=region,
                guild=guild,
                class_name=class_name,
                spec=spec,
            )
            self.session.add(character)
            await self.session.flush()
            logger.info(f"Created character: {name}-{realm}")
            return character
        except Exception as e:
            logger.error(f"Failed to create character: {e}")
            raise DatabaseError(f"Failed to create character: {e}")

    async def update_character(self, character_id: int, **kwargs) -> Optional[Character]:
        """Update character.
        
        Args:
            character_id: Character database ID
            **kwargs: Fields to update
            
        Returns:
            Updated Character instance or None
        """
        try:
            character = await self.get_character(character_id)
            if not character:
                return None

            for key, value in kwargs.items():
                if hasattr(character, key):
                    setattr(character, key, value)

            await self.session.flush()
            logger.info(f"Updated character: {character_id}")
            return character
        except Exception as e:
            logger.error(f"Failed to update character: {e}")
            raise DatabaseError(f"Failed to update character: {e}")

    async def delete_character(self, character_id: int) -> bool:
        """Delete character.
        
        Args:
            character_id: Character database ID
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            character = await self.get_character(character_id)
            if not character:
                return False

            await self.session.delete(character)
            await self.session.flush()
            logger.info(f"Deleted character: {character_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete character: {e}")
            raise DatabaseError(f"Failed to delete character: {e}")
