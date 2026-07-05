"""Verification embeds."""

import discord

from src.config.constants import DiscordColor


def create_verification_start_embed() -> discord.Embed:
    """Create verification start embed.
    
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title="🔐 Character Verification",
        description="Let's verify your World of Warcraft character!",
        color=DiscordColor.PRIMARY.value,
    )
    embed.add_field(
        name="How it works:",
        value="1. Provide your character name\n2. Select your realm\n3. Select your region\n4. We'll verify your character and assign roles!",
        inline=False,
    )
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed


def create_verification_success_embed(character_name: str, realm: str) -> discord.Embed:
    """Create verification success embed.
    
    Args:
        character_name: Character name
        realm: Realm name
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title="✅ Verification Successful",
        description=f"Welcome, {character_name}!",
        color=DiscordColor.SUCCESS.value,
    )
    embed.add_field(name="Character", value=f"{character_name}-{realm}", inline=True)
    embed.add_field(name="Status", value="Verified ✓", inline=True)
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed


def create_verification_error_embed(error_message: str) -> discord.Embed:
    """Create verification error embed.
    
    Args:
        error_message: Error message
        
    Returns:
        Discord embed
    """
    embed = discord.Embed(
        title="❌ Verification Failed",
        description=error_message,
        color=DiscordColor.DANGER.value,
    )
    embed.add_field(
        name="What to check:",
        value="• Character name spelling\n• Correct realm name\n• Correct region selection\n• Character must exist on Battle.net",
        inline=False,
    )
    embed.set_footer(text="LogRun • World of Warcraft Guild Management")
    return embed
