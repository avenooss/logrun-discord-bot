"""Role management service."""

import logging
from typing import List, Optional

import discord

from src.config.constants import PERFORMANCE_TIERS, WOW_CLASSES
from src.utils.helpers import calculate_percentile_tier

logger = logging.getLogger(__name__)


class RoleManager:
    """Service for managing Discord roles."""

    @staticmethod
    async def get_rank_role_name(performance: float) -> str:
        """Get rank role name based on performance.
        
        Args:
            performance: Performance percentile (0-100)
            
        Returns:
            Rank role name
        """
        return calculate_percentile_tier(performance)

    @staticmethod
    async def assign_rank_role(
        member: discord.Member, guild: discord.Guild, role_name: str
    ) -> bool:
        """Assign rank role to member.
        
        Args:
            member: Discord member
            guild: Discord guild
            role_name: Role name to assign
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find role by name
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                logger.warning(f"Role not found: {role_name}")
                return False

            # Remove other rank roles
            for rank_name in PERFORMANCE_TIERS.keys():
                rank_role = discord.utils.get(guild.roles, name=rank_name)
                if rank_role and rank_role in member.roles:
                    await member.remove_roles(rank_role)

            # Add new rank role
            await member.add_roles(role)
            logger.info(f"Assigned role {role_name} to {member}")
            return True
        except discord.Forbidden:
            logger.error(f"Permission denied assigning role to {member}")
            return False
        except Exception as e:
            logger.error(f"Failed to assign role: {e}")
            return False

    @staticmethod
    async def assign_class_role(
        member: discord.Member, guild: discord.Guild, class_name: str
    ) -> bool:
        """Assign class role to member.
        
        Args:
            member: Discord member
            guild: Discord guild
            class_name: WoW class name
            
        Returns:
            True if successful, False otherwise
        """
        if class_name not in WOW_CLASSES:
            logger.warning(f"Invalid class: {class_name}")
            return False

        try:
            # Find role by name
            role = discord.utils.get(guild.roles, name=class_name)
            if not role:
                logger.warning(f"Role not found: {class_name}")
                return False

            # Remove other class roles
            for wow_class in WOW_CLASSES:
                class_role = discord.utils.get(guild.roles, name=wow_class)
                if class_role and class_role in member.roles:
                    await member.remove_roles(class_role)

            # Add class role
            await member.add_roles(role)
            logger.info(f"Assigned class role {class_name} to {member}")
            return True
        except discord.Forbidden:
            logger.error(f"Permission denied assigning class role to {member}")
            return False
        except Exception as e:
            logger.error(f"Failed to assign class role: {e}")
            return False

    @staticmethod
    async def remove_all_roles(
        member: discord.Member, guild: discord.Guild, role_names: List[str]
    ) -> bool:
        """Remove multiple roles from member.
        
        Args:
            member: Discord member
            guild: Discord guild
            role_names: List of role names to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            roles_to_remove = []
            for role_name in role_names:
                role = discord.utils.get(guild.roles, name=role_name)
                if role and role in member.roles:
                    roles_to_remove.append(role)

            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                logger.info(f"Removed {len(roles_to_remove)} roles from {member}")

            return True
        except discord.Forbidden:
            logger.error(f"Permission denied removing roles from {member}")
            return False
        except Exception as e:
            logger.error(f"Failed to remove roles: {e}")
            return False

    @staticmethod
    async def create_role(
        guild: discord.Guild,
        name: str,
        color: Optional[discord.Color] = None,
        permissions: Optional[discord.Permissions] = None,
        reason: Optional[str] = None,
    ) -> Optional[discord.Role]:
        """Create a new role in guild.
        
        Args:
            guild: Discord guild
            name: Role name
            color: Role color
            permissions: Role permissions
            reason: Reason for creation
            
        Returns:
            Created role or None
        """
        try:
            role = await guild.create_role(
                name=name, color=color, permissions=permissions, reason=reason
            )
            logger.info(f"Created role: {name}")
            return role
        except discord.Forbidden:
            logger.error(f"Permission denied creating role: {name}")
            return None
        except Exception as e:
            logger.error(f"Failed to create role: {e}")
            return None
