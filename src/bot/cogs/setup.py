"""Server setup commands cog."""

import logging

import discord
from discord.ext import commands

from src.services.guild_manager import GuildManager
from src.services.role_manager import RoleManager
from src.config.constants import WOW_CLASSES, PERFORMANCE_TIERS, ROLE_TYPES, ADMIN_ROLES

logger = logging.getLogger(__name__)


class SetupCog(commands.Cog):
    """Server setup commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog.
        
        Args:
            bot: Discord bot instance
        """
        self.bot = bot

    @discord.app_commands.command(
        name="setup", description="Initialize server with categories, channels, and roles"
    )
    @discord.app_commands.default_permissions(administrator=True)
    async def setup(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Setup server structure.
        
        Args:
            interaction: Discord interaction
        """
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ This command can only be used in a guild", ephemeral=True
            )
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need administrator permissions", ephemeral=True
            )
            return

        await interaction.response.defer()

        try:
            # Create server structure
            await GuildManager.create_server_structure(interaction.guild)

            # Create rank roles
            for rank_name in PERFORMANCE_TIERS.keys():
                await RoleManager.create_role(
                    interaction.guild,
                    rank_name,
                    reason="LogRun setup",
                )

            # Create class roles
            for class_name in WOW_CLASSES:
                await RoleManager.create_role(
                    interaction.guild,
                    class_name,
                    reason="LogRun setup",
                )

            # Create role type roles
            for role_type in ROLE_TYPES:
                await RoleManager.create_role(
                    interaction.guild,
                    role_type,
                    reason="LogRun setup",
                )

            # Create admin roles
            for admin_role in ADMIN_ROLES:
                await RoleManager.create_role(
                    interaction.guild,
                    admin_role,
                    reason="LogRun setup",
                )

            embed = discord.Embed(
                title="✅ Server Setup Complete",
                description="Your server has been configured!",
                color=discord.Color.green(),
            )
            embed.add_field(
                name="Created:",
                value="✓ Categories and channels\n✓ Rank roles\n✓ Class roles\n✓ Type roles\n✓ Admin roles",
                inline=False,
            )
            embed.set_footer(text="LogRun • World of Warcraft Guild Management")

            await interaction.followup.send(embed=embed)
            logger.info(f"Server setup completed for {interaction.guild.name}")

        except Exception as e:
            logger.error(f"Setup error: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Setup failed: {str(e)}", ephemeral=True
            )

    @discord.app_commands.command(
        name="delete_all",
        description="Delete all bot-created structures (use with caution!)",
    )
    @discord.app_commands.default_permissions(administrator=True)
    async def delete_all(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Delete all bot-created structures.
        
        Args:
            interaction: Discord interaction
        """
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ This command can only be used in a guild", ephemeral=True
            )
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need administrator permissions", ephemeral=True
            )
            return

        await interaction.response.defer()

        try:
            await GuildManager.delete_all_structures(interaction.guild)

            embed = discord.Embed(
                title="✅ Cleanup Complete",
                description="All bot-created structures have been removed.",
                color=discord.Color.green(),
            )
            await interaction.followup.send(embed=embed)
            logger.info(f"Cleanup completed for {interaction.guild.name}")

        except Exception as e:
            logger.error(f"Cleanup error: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Cleanup failed: {str(e)}", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """Setup cog.
    
    Args:
        bot: Discord bot instance
    """
    await bot.add_cog(SetupCog(bot))
