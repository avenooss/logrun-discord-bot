"""Verification service for player authentication."""

import logging
from typing import Optional, Tuple

from src.database.repositories.character import CharacterRepository
from src.database.repositories.user import UserRepository
from src.services.battle_net import BattleNetClient
from src.services.warcraft_logs import WarcraftLogsClient
from src.utils.errors import VerificationError
from src.utils.helpers import get_timestamp
from src.utils.validators import (
    validate_character_name,
    validate_realm_name,
    validate_region,
)

logger = logging.getLogger(__name__)


class VerificationService:
    """Service for verifying player characters."""

    def __init__(
        self,
        user_repo: UserRepository,
        character_repo: CharacterRepository,
        warcraft_logs_client: WarcraftLogsClient,
        battle_net_client: BattleNetClient,
    ):
        """Initialize verification service.
        
        Args:
            user_repo: User repository
            character_repo: Character repository
            warcraft_logs_client: Warcraft Logs API client
            battle_net_client: Battle.net API client
        """
        self.user_repo = user_repo
        self.character_repo = character_repo
        self.warcraft_logs_client = warcraft_logs_client
        self.battle_net_client = battle_net_client

    async def verify_character(
        self, discord_id: int, character_name: str, realm_name: str, region: str
    ) -> Tuple[bool, Optional[str]]:
        """Verify a character exists and belongs to player.
        
        Args:
            discord_id: Discord user ID
            character_name: Character name
            realm_name: Realm name
            region: Region code
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        # Validate inputs
        if not validate_character_name(character_name):
            return False, "Invalid character name format"
        if not validate_realm_name(realm_name):
            return False, "Invalid realm name format"
        if not validate_region(region):
            return False, "Invalid region"

        try:
            # Check if character exists on Battle.net
            exists = await self.battle_net_client.verify_character_exists(
                character_name, realm_name, region
            )
            if not exists:
                return False, "Character not found on Battle.net"

            # Get character profile
            profile = await self.battle_net_client.get_character_profile(
                character_name, realm_name, region
            )

            # Create or update character in database
            character = await self.character_repo.get_character_by_name(
                character_name, realm_name, region
            )

            if character:
                await self.character_repo.update_character(
                    character.id,
                    discord_id=discord_id,
                    class_name=profile.get("character_class", {}).get("name"),
                    level=profile.get("level"),
                    updated_at=get_timestamp(),
                )
            else:
                await self.character_repo.create_character(
                    discord_id=discord_id,
                    name=character_name,
                    realm=realm_name,
                    region=region,
                    class_name=profile.get("character_class", {}).get("name"),
                )

            logger.info(f"Character verified: {character_name}-{realm_name}")
            return True, None

        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False, f"Verification failed: {str(e)}"

    async def get_character_performance(
        self, character_name: str, realm_name: str, region: str
    ) -> Optional[float]:
        """Get character performance from Warcraft Logs.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code
            
        Returns:
            Performance percentile or None
        """
        try:
            data = await self.warcraft_logs_client.query_character_performance(
                character_name, realm_name, region
            )

            # Extract heroic best performance average
            character_data = data.get("characterData", {}).get("character")
            if not character_data:
                return None

            raid_ranks = character_data.get("raidRanks", [])
            if raid_ranks and raid_ranks[0].get("bestPerf"):
                return raid_ranks[0]["bestPerf"].get("percentile", 0.0)

            return 0.0
        except Exception as e:
            logger.error(f"Failed to get performance: {e}")
            return None
