"""Statistics embeds."""

import discord

from src.config.constants import DiscordColor


def create_guild_stats_embed(
    guild_name: str,
    total_members: int,
    verified_members: int,
    avg_performance: float,
    raider_elite_count: int,
    raider_count: int,
    casual_count: int,
) -> discord.Embed:
    """Create guild statistics embed.
    
    Args:
        guild_name: Guild name
        total_members: Total member count
        verified_members: Verified member count
        avg_performance: Average performance
        raider_elite_count: Raider Elite role count
        raider_count: Raider role count
        casual_count: Casual role count
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title=f"📊 {guild_name} Statistics",
        description="Guild-wide performance overview",
        color=DiscordColor.INFO.value,
    )

    verification_rate = (
        (verified_members / total_members * 100) if total_members > 0 else 0
    )
    embed.add_field(
        name="Members",
        value=f"Total: {total_members}\nVerified: {verified_members} ({verification_rate:.1f}%)",
        inline=True,
    )
    embed.add_field(
        name="Average Performance",
        value=f"{avg_performance:.1f}%",
        inline=True,
    )
    embed.add_field(
        name="Role Distribution",
        value=f"🏅 Elite: {raider_elite_count}\n⭐ Raider: {raider_count}\n👥 Casual: {casual_count}",
        inline=False,
    )
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed


def create_class_stats_embed(class_name: str, data: dict) -> discord.Embed:
    """Create class statistics embed.
    
    Args:
        class_name: WoW class name
        data: Statistics data
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title=f"📊 {class_name} Statistics",
        description=f"{class_name} role distribution and performance",
        color=DiscordColor.INFO.value,
    )

    total = data.get("total", 0)
    avg_perf = data.get("avg_performance", 0)
    specs = data.get("specs", {})

    embed.add_field(name="Total Members", value=str(total), inline=True)
    embed.add_field(name="Average Performance", value=f"{avg_perf:.1f}%", inline=True)

    spec_text = ""
    for spec, count in specs.items():
        spec_text += f"{spec}: {count}\n"

    if spec_text:
        embed.add_field(name="Specialization Distribution", value=spec_text, inline=False)

    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed
