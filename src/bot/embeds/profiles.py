"""Profile embeds."""

from typing import Optional

import discord

from src.config.constants import DiscordColor


def create_profile_embed(
    character_name: str,
    realm: str,
    class_name: str,
    spec: str,
    performance: float,
    rank_role: str,
    level: int = 70,
    item_level: Optional[int] = None,
) -> discord.Embed:
    """Create player profile embed.
    
    Args:
        character_name: Character name
        realm: Realm name
        class_name: Character class
        spec: Character specialization
        performance: Performance percentile
        rank_role: Rank role name
        level: Character level
        item_level: Item level
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title=f"{character_name}",
        description=f"{class_name} {spec} • {realm}",
        color=DiscordColor.PRIMARY.value,
    )

    embed.add_field(name="Level", value=str(level), inline=True)
    if item_level:
        embed.add_field(name="Item Level", value=str(item_level), inline=True)
    embed.add_field(name="Region", value="US", inline=True)

    embed.add_field(
        name="Performance",
        value=f"{performance:.1f}% • {rank_role}",
        inline=False,
    )

    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed


def create_character_not_found_embed(search_query: str) -> discord.Embed:
    """Create character not found embed.
    
    Args:
        search_query: Search query
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title="❌ Character Not Found",
        description=f"Could not find character: {search_query}",
        color=DiscordColor.DANGER.value,
    )
    embed.add_field(
        name="Try:",
        value="• Check character name spelling\n• Verify realm name\n• Make sure character exists",
        inline=False,
    )
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed
