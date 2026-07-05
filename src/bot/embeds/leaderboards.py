"""Leaderboard embeds."""

from typing import List, Tuple

import discord

from src.config.constants import DiscordColor
from src.utils.helpers import get_ordinal_suffix


def create_leaderboard_embed(
    entries: List[Tuple[int, str, float, str]], title: str = "Guild Leaderboard"
) -> discord.Embed:
    """Create leaderboard embed.
    
    Args:
        entries: List of (rank, character_name, performance, class_name) tuples
        title: Embed title
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title=f"🏆 {title}",
        description="Top performers in the guild",
        color=DiscordColor.GOLD.value,
    )

    leaderboard_text = ""
    for rank, character_name, performance, class_name in entries:
        ordinal = get_ordinal_suffix(rank)
        leaderboard_text += f"{ordinal} • {character_name} ({class_name})\n"
        leaderboard_text += f"┗━ {performance:.1f}%\n"

    embed.add_field(name="Rankings", value=leaderboard_text or "No data yet", inline=False)
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed


def create_class_leaderboard_embed(
    class_name: str, entries: List[Tuple[int, str, float]]
) -> discord.Embed:
    """Create class-specific leaderboard embed.
    
    Args:
        class_name: WoW class name
        entries: List of (rank, character_name, performance) tuples
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title=f"🏆 {class_name} Leaderboard",
        description=f"Top {class_name} performers",
        color=DiscordColor.GOLD.value,
    )

    leaderboard_text = ""
    for rank, character_name, performance in entries:
        ordinal = get_ordinal_suffix(rank)
        leaderboard_text += f"{ordinal} • {character_name}\n"
        leaderboard_text += f"┗━ {performance:.1f}%\n"

    embed.add_field(name="Rankings", value=leaderboard_text or "No data yet", inline=False)
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed
