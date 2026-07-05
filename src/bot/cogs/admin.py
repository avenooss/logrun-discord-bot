"""Admin commands cog."""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    """Admin commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog.
        
        Args:
            bot: Discord bot instance
        """
        self.bot = bot

    @discord.app_commands.command(
        name="admin", description="Access admin panel"
    )
    @discord.app_commands.default_permissions(administrator=True)
    async def admin(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Access admin panel.
        
        Args:
            interaction: Discord interaction
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need administrator permissions", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="⚙️ Admin Panel",
            description="Admin controls coming soon!",
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin panel accessed by {interaction.user}")

    @discord.app_commands.command(
        name="export", description="Export guild data"
    )
    @discord.app_commands.default_permissions(administrator=True)
    async def export(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Export guild data.
        
        Args:
            interaction: Discord interaction
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need administrator permissions", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            "Export command coming soon!", ephemeral=True
        )
        logger.info(f"Export command executed by {interaction.user}")

    @discord.app_commands.command(
        name="import", description="Import guild data"
    )
    @discord.app_commands.default_permissions(administrator=True)
    async def import_data(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Import guild data.
        
        Args:
            interaction: Discord interaction
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need administrator permissions", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            "Import command coming soon!", ephemeral=True
        )
        logger.info(f"Import command executed by {interaction.user}")


async def setup(bot: commands.Bot) -> None:
    """Setup cog.
    
    Args:
        bot: Discord bot instance
    """
    await bot.add_cog(AdminCog(bot))
