"""Verification commands cog."""

import logging

import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.embeds.verification import (
    create_verification_error_embed,
    create_verification_start_embed,
    create_verification_success_embed,
)
from src.database.connection import AsyncSessionLocal
from src.database.repositories.character import CharacterRepository
from src.database.repositories.user import UserRepository
from src.services.battle_net import BattleNetClient
from src.services.role_manager import RoleManager
from src.services.verification import VerificationService
from src.services.warcraft_logs import WarcraftLogsClient

logger = logging.getLogger(__name__)


class VerificationCog(commands.Cog):
    """Character verification commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog.
        
        Args:
            bot: Discord bot instance
        """
        self.bot = bot

    @discord.app_commands.command(
        name="verify", description="Verify your World of Warcraft character"
    )
    @discord.app_commands.describe(
        character_name="Your character name",
        realm_name="Your realm name",
        region="Region (us, eu, kr, tw, cn)",
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        character_name: str,
        realm_name: str,
        region: str,
    ) -> None:
        """Verify a World of Warcraft character.
        
        Args:
            interaction: Discord interaction
            character_name: Character name
            realm_name: Realm name
            region: Region code
        """
        await interaction.response.defer(ephemeral=True)

        try:
            async with AsyncSessionLocal() as session:
                user_repo = UserRepository(session)
                character_repo = CharacterRepository(session)
                warcraft_logs_client = WarcraftLogsClient()
                battle_net_client = BattleNetClient()

                async with warcraft_logs_client, battle_net_client:
                    verification_service = VerificationService(
                        user_repo,
                        character_repo,
                        warcraft_logs_client,
                        battle_net_client,
                    )

                    # Verify character
                    success, error = await verification_service.verify_character(
                        interaction.user.id, character_name, realm_name, region
                    )

                    if not success:
                        embed = create_verification_error_embed(error or "Unknown error")
                        await interaction.followup.send(embed=embed, ephemeral=True)
                        return

                    # Get or create user
                    user = await user_repo.get_user(interaction.user.id)
                    if not user:
                        user = await user_repo.create_user(
                            interaction.user.id,
                            interaction.user.name,
                            str(interaction.user),
                        )

                    # Mark as verified
                    await user_repo.mark_verified(interaction.user.id)

                    # Assign roles
                    if interaction.guild:
                        member = interaction.guild.get_member(interaction.user.id)
                        if member:
                            # Get character performance
                            perf = await verification_service.get_character_performance(
                                character_name, realm_name, region
                            )

                            if perf is not None:
                                rank_role = await RoleManager.get_rank_role_name(perf)
                                await RoleManager.assign_rank_role(
                                    member, interaction.guild, rank_role
                                )

                    await session.commit()

                    embed = create_verification_success_embed(character_name, realm_name)
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    logger.info(
                        f"Verification successful for {interaction.user}: {character_name}"
                    )

        except Exception as e:
            logger.error(f"Verification error: {e}", exc_info=True)
            embed = create_verification_error_embed("An unexpected error occurred")
            await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.app_commands.command(
        name="refresh", description="Manually refresh your performance data"
    )
    async def refresh(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """Manually refresh performance data.
        
        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            "Refresh command coming soon!", ephemeral=True
        )
        logger.info(f"Refresh command executed by {interaction.user}")


async def setup(bot: commands.Bot) -> None:
    """Setup cog.
    
    Args:
        bot: Discord bot instance
    """
    await bot.add_cog(VerificationCog(bot))
