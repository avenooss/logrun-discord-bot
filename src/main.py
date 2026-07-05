"""Main entry point for LogRun bot."""

import asyncio
import logging
import sys
from pathlib import Path

from src.bot.bot import LogRunBot
from src.config.settings import settings
from src.utils.logger import setup_logging


async def main() -> None:
    """Start the LogRun bot."""
    setup_logging(settings.LOG_LEVEL)
    logger = logging.getLogger(__name__)

    logger.info(f"LogRun Bot v{settings.version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database_url}")

    bot = LogRunBot()
    
    try:
        async with bot:
            await bot.start(settings.discord_token)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Bot startup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
