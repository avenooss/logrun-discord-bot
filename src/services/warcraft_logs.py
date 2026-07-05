"""Warcraft Logs API client service."""

import logging
from datetime import datetime, timedelta
from typing import Optional

import aiohttp

from src.config.constants import WARCRAFT_LOGS_API_URL, WARCRAFT_LOGS_OAUTH_URL
from src.config.settings import settings
from src.utils.errors import RateLimitError, WarcraftLogsError

logger = logging.getLogger(__name__)


class WarcraftLogsClient:
    """Warcraft Logs API client."""

    def __init__(self):
        """Initialize Warcraft Logs client."""
        self.client_id = settings.warcraft_logs_client_id
        self.client_secret = settings.warcraft_logs_client_secret
        self.token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "WarcraftLogsClient":
        """Context manager entry."""
        self.session = aiohttp.ClientSession()
        await self._get_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        if self.session:
            await self.session.close()

    async def _get_token(self) -> str:
        """Get OAuth2 token from Warcraft Logs.
        
        Returns:
            Access token
            
        Raises:
            WarcraftLogsError: If token retrieval fails
        """
        if self.token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.token

        try:
            async with self.session.post(
                WARCRAFT_LOGS_OAUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            ) as response:
                if response.status == 401:
                    raise WarcraftLogsError(
                        "Invalid Warcraft Logs credentials", "INVALID_CREDENTIALS"
                    )
                if response.status == 429:
                    raise RateLimitError(
                        "Warcraft Logs rate limit exceeded", "RATE_LIMIT_EXCEEDED"
                    )
                if response.status != 200:
                    raise WarcraftLogsError(
                        f"Token request failed: {response.status}", "TOKEN_REQUEST_FAILED"
                    )

                data = await response.json()
                self.token = data["access_token"]
                expires_in = data.get("expires_in", 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                logger.info("Warcraft Logs token obtained")
                return self.token
        except aiohttp.ClientError as e:
            raise WarcraftLogsError(f"Failed to get token: {e}", "CONNECTION_ERROR")

    async def query_character_performance(
        self, character_name: str, realm_name: str, region: str
    ) -> dict:
        """Query character performance from Warcraft Logs.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code (us, eu, kr, tw, cn)
            
        Returns:
            Character performance data
            
        Raises:
            WarcraftLogsError: If query fails
        """
        await self._get_token()

        query = """
        query {
            characterData {
                character(name: "%s", serverRegion: "%s", serverSlug: "%s") {
                    name
                    class
                    classID
                    spec
                    specID
                    level
                    gender
                    race
                    raceID
                    guild {
                        name
                        realm
                    }
                    mythicPlusRanks {
                        overall {
                            rank
                            percentile
                        }
                    }
                    raidRanks(difficulty: "Heroic") {
                        bestPerf {
                            percentile
                        }
                    }
                }
            }
        }
        """ % (
            character_name,
            region.upper(),
            realm_name.lower().replace(" ", "-"),
        )

        try:
            async with self.session.post(
                WARCRAFT_LOGS_API_URL,
                json={"query": query},
                headers={"Authorization": f"Bearer {self.token}"},
            ) as response:
                if response.status == 429:
                    raise RateLimitError(
                        "Warcraft Logs rate limit exceeded", "RATE_LIMIT_EXCEEDED"
                    )
                if response.status != 200:
                    raise WarcraftLogsError(
                        f"Query failed: {response.status}", "QUERY_FAILED"
                    )

                data = await response.json()
                if "errors" in data:
                    error_msg = data["errors"][0].get("message", "Unknown error")
                    raise WarcraftLogsError(f"GraphQL error: {error_msg}", "GRAPHQL_ERROR")

                return data.get("data", {})
        except aiohttp.ClientError as e:
            raise WarcraftLogsError(f"Query failed: {e}", "CONNECTION_ERROR")

    async def get_character_rankings(
        self, character_name: str, realm_name: str, region: str
    ) -> dict:
        """Get character rankings.
        
        Args:
            character_name: Character name
            realm_name: Realm name
            region: Region code
            
        Returns:
            Character rankings data
            
        Raises:
            WarcraftLogsError: If query fails
        """
        return await self.query_character_performance(character_name, realm_name, region)
