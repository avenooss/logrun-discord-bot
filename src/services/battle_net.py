"""Battle.net API client service."""

import logging
from typing import Optional

import aiohttp

from src.config.constants import BATTLENET_API_BASE_URL
from src.config.settings import settings
from src.utils.errors import BattleNetError, RateLimitError

logger = logging.getLogger(__name__)


class BattleNetClient:
    """Battle.net API client."""

    def __init__(self):
        """Initialize Battle.net client."""
        self.api_key = settings.battlenet_api_key
        self.region = settings.battlenet_region
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "BattleNetClient":
        """Context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        if self.session:
            await self.session.close()

    def _get_base_url(self, region: Optional[str] = None) -> str:
        """Get Battle.net API base URL for region.
        
        Args:
            region: Region code (defaults to configured region)
            
        Returns:
            Base URL for API region
        """
        region = region or self.region
        return BATTLENET_API_BASE_URL.format(region=region)

    async def get_character_profile(
        self, character_name: str, realm_name: str, region: Optional[str] = None
    ) -> dict:
        """Get character profile from Battle.net.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code (defaults to configured region)
            
        Returns:
            Character profile data
            
        Raises:
            BattleNetError: If query fails
        """
        base_url = self._get_base_url(region)
        url = f"{base_url}/profile/wow/character/{realm_name.lower().replace(' ', '-')}/{character_name.lower()}"

        params = {"namespace": "profile-{}".format(region or self.region), "locale": "en_US"}

        try:
            async with self.session.get(
                url, params={**params, "access_token": self.api_key}
            ) as response:
                if response.status == 404:
                    raise BattleNetError(
                        f"Character not found: {character_name}-{realm_name}",
                        "CHARACTER_NOT_FOUND",
                    )
                if response.status == 429:
                    raise RateLimitError(
                        "Battle.net rate limit exceeded", "RATE_LIMIT_EXCEEDED"
                    )
                if response.status != 200:
                    raise BattleNetError(
                        f"Profile request failed: {response.status}", "REQUEST_FAILED"
                    )

                return await response.json()
        except aiohttp.ClientError as e:
            raise BattleNetError(f"Profile request failed: {e}", "CONNECTION_ERROR")

    async def get_character_statistics(
        self, character_name: str, realm_name: str, region: Optional[str] = None
    ) -> dict:
        """Get character statistics.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code
            
        Returns:
            Character statistics
            
        Raises:
            BattleNetError: If query fails
        """
        base_url = self._get_base_url(region)
        url = f"{base_url}/profile/wow/character/{realm_name.lower().replace(' ', '-')}/{character_name.lower()}/statistics"

        params = {"namespace": "profile-{}".format(region or self.region), "locale": "en_US"}

        try:
            async with self.session.get(
                url, params={**params, "access_token": self.api_key}
            ) as response:
                if response.status == 404:
                    raise BattleNetError(
                        "Statistics not found", "NOT_FOUND"
                    )
                if response.status == 429:
                    raise RateLimitError(
                        "Battle.net rate limit exceeded", "RATE_LIMIT_EXCEEDED"
                    )
                if response.status != 200:
                    raise BattleNetError(
                        f"Statistics request failed: {response.status}", "REQUEST_FAILED"
                    )

                return await response.json()
        except aiohttp.ClientError as e:
            raise BattleNetError(f"Statistics request failed: {e}", "CONNECTION_ERROR")

    async def verify_character_exists(
        self, character_name: str, realm_name: str, region: Optional[str] = None
    ) -> bool:
        """Verify that a character exists.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code
            
        Returns:
            True if character exists, False otherwise
        """
        try:
            await self.get_character_profile(character_name, realm_name, region)
            return True
        except BattleNetError as e:
            if e.code == "CHARACTER_NOT_FOUND":
                return False
            raise
