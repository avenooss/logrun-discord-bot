"""Info commands cog."""

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class InfoCog(commands.Cog):
    """Information and help commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog.
        
        Args:
            bot: Discord bot instance
        """
        self.bot = bot

    @discord.app_commands.command(name="help", description="Display help information")
    async def help(self, interaction: discord.Interaction) -> None:
        """Display help information.
        
        Args:
            interaction: Discord interaction
        """
        embed = discord.Embed(
            title="🆘 LogRun Commands",
            description="Complete command reference",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="🔐 Verification",
            value="`/verify` - Link your Battle.net account\n`/mylog` - View your performance",
            inline=False,
        )

        embed.add_field(
            name="👤 Profile",
            value="`/profile` - View your guild profile\n`/leaderboard` - View guild leaderboards",
            inline=False,
        )

        embed.add_field(
            name="📊 Statistics",
            value="`/stats` - View guild statistics\n`/class` - View class statistics",
            inline=False,
        )

        embed.add_field(
            name="⚙️ Admin",
            value="`/setup` - Initialize server\n`/refresh` - Update performance data\n`/admin` - Admin panel",
            inline=False,
        )

        embed.set_footer(text="LogRun • World of Warcraft Guild Management")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Help command executed by {interaction.user}")

    @discord.app_commands.command(
        name="ping", description="Check bot latency"
    )
    async def ping(self, interaction: discord.Interaction) -> None:
        """Check bot latency.
        
        Args:
            interaction: Discord interaction
        """
        latency = self.bot.latency * 1000
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency:.0f}ms",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Ping command executed by {interaction.user}")


async def setup(bot: commands.Bot) -> None:
    """Setup cog.
    
    Args:
        bot: Discord bot instance
    """
    await bot.add_cog(InfoCog(bot))
