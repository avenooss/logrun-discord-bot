"""Guild management service."""

import logging
from typing import Optional

import discord

from src.config.constants import CATEGORIES, CHANNELS

logger = logging.getLogger(__name__)


class GuildManager:
    """Service for managing Discord guild structure."""

    @staticmethod
    async def create_server_structure(guild: discord.Guild) -> bool:
        """Create the complete server structure with categories and channels.
        
        Args:
            guild: Discord guild
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create categories and channels
            for category_name, category_desc in CATEGORIES.items():
                # Create category
                category = await guild.create_category(
                    name=category_name, reason="LogRun server setup"
                )
                logger.info(f"Created category: {category_name}")

                # Create channels in category
                if category_name in CHANNELS:
                    for channel_name, channel_desc in CHANNELS[category_name]:
                        await guild.create_text_channel(
                            name=channel_name,
                            category=category,
                            topic=channel_desc,
                            reason="LogRun server setup",
                        )
                        logger.info(f"Created channel: {channel_name}")

            logger.info(f"Server structure created for {guild.name}")
            return True
        except discord.Forbidden:
            logger.error(f"Permission denied creating server structure")
            return False
        except Exception as e:
            logger.error(f"Failed to create server structure: {e}")
            return False

    @staticmethod
    async def get_or_create_category(
        guild: discord.Guild, name: str
    ) -> Optional[discord.CategoryChannel]:
        """Get existing category or create new one.
        
        Args:
            guild: Discord guild
            name: Category name
            
        Returns:
            Category channel or None
        """
        try:
            # Check if category exists
            category = discord.utils.get(guild.categories, name=name)
            if category:
                return category

            # Create new category
            category = await guild.create_category(name=name, reason="LogRun")
            logger.info(f"Created category: {name}")
            return category
        except discord.Forbidden:
            logger.error(f"Permission denied creating category: {name}")
            return None
        except Exception as e:
            logger.error(f"Failed to create category: {e}")
            return None

    @staticmethod
    async def get_or_create_channel(
        guild: discord.Guild,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
    ) -> Optional[discord.TextChannel]:
        """Get existing channel or create new one.
        
        Args:
            guild: Discord guild
            name: Channel name
            category: Parent category (optional)
            
        Returns:
            Text channel or None
        """
        try:
            # Check if channel exists
            channel = discord.utils.get(guild.text_channels, name=name)
            if channel:
                return channel

            # Create new channel
            channel = await guild.create_text_channel(
                name=name, category=category, reason="LogRun"
            )
            logger.info(f"Created channel: {name}")
            return channel
        except discord.Forbidden:
            logger.error(f"Permission denied creating channel: {name}")
            return None
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            return None

    @staticmethod
    async def delete_all_structures(guild: discord.Guild) -> bool:
        """Delete all bot-created structures (categories and channels).
        
        Args:
            guild: Discord guild
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete all categories
            for category in guild.categories:
                if category.name in CATEGORIES:
                    await category.delete(reason="LogRun cleanup")
                    logger.info(f"Deleted category: {category.name}")

            logger.info(f"Deleted all structures from {guild.name}")
            return True
        except discord.Forbidden:
            logger.error(f"Permission denied deleting structures")
            return False
        except Exception as e:
            logger.error(f"Failed to delete structures: {e}")
            return False
