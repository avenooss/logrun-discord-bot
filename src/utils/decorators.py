"""Custom decorators for the bot."""

import functools
import logging
from typing import Any, Callable, TypeVar

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Callable[..., Any])


def require_guild() -> Callable[[T], T]:
    """Decorator to require command to be used in a guild."""
    async def predicate(ctx: commands.Context) -> bool:
        if not ctx.guild:
            await ctx.send("❌ This command can only be used in a guild.")
            return False
        return True

    return commands.check(predicate)


def require_permissions(**perms: bool) -> Callable[[T], T]:
    """Decorator to require specific permissions.
    
    Args:
        **perms: Permissions to require (e.g., manage_messages=True)
    """
    async def predicate(ctx: commands.Context) -> bool:
        if not isinstance(ctx.author, discord.Member):
            return False
        
        if ctx.author == ctx.guild.owner:
            return True
        
        missing = []
        for perm, required in perms.items():
            if required and not getattr(ctx.author.guild_permissions, perm, False):
                missing.append(perm)
        
        if missing:
            perm_str = ", ".join(missing)
            await ctx.send(f"❌ You need the following permissions: {perm_str}")
            return False
        
        return True

    return commands.check(predicate)


def log_command(func: T) -> T:
    """Decorator to log command execution."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Executing command: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Command completed: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Command failed: {func.__name__} - {e}", exc_info=True)
            raise

    return wrapper


def handle_errors(func: T) -> T:
    """Decorator to handle errors in async functions."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper
