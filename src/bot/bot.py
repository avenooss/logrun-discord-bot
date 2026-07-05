"""Main Discord bot initialization and event handlers."""

import logging
from typing import Optional

import discord
from discord.ext import commands

from src.config.settings import settings
from src.database.connection import close_db, init_db
from src.services.cache import CacheManager
from src.services.scheduler import Scheduler

logger = logging.getLogger(__name__)


class LogRunBot(commands.Bot):
    """LogRun Discord bot."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.guild_messages = True
        intents.direct_messages = True
        intents.guild_reactions = True

        super().__init__(
            command_prefix=settings.bot_prefix,
            intents=intents,
            help_command=None,
            *args,
            **kwargs,
        )

        self.cache = CacheManager(default_ttl=settings.cache_ttl)
        self.scheduler = Scheduler()
        self.synced = False

    async def setup_hook(self) -> None:
        """Setup hook called before connect."""
        logger.info("Setting up bot...")

        # Initialize database
        await init_db()

        # Load cogs
        await self._load_cogs()

        logger.info("Bot setup complete")

    async def on_ready(self) -> None:
        """Called when bot is ready."""
        logger.info(f"Logged in as {self.user}")
        logger.info(f"Syncing commands...")

        if not self.synced:
            await self.tree.sync()
            self.synced = True
            logger.info("Commands synced")

        # Start scheduler
        if not self.scheduler.running:
            await self.scheduler.start()
            logger.info("Scheduler started")

        activity = discord.Activity(
            type=discord.ActivityType.watching, name="Warcraft Logs"
        )
        await self.change_presence(activity=activity)

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Handle bot errors."""
        logger.error(f"Error in {event}", exc_info=True)

    async def close(self) -> None:
        """Close bot connection."""
        await self.scheduler.stop()
        await close_db()
        await super().close()

    async def _load_cogs(self) -> None:
        """Load all cogs."""
        cogs = [
            "src.bot.cogs.info",
            "src.bot.cogs.verification",
            "src.bot.cogs.guild",
            "src.bot.cogs.setup",
            "src.bot.cogs.admin",
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}", exc_info=True)
