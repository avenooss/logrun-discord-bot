"""SQLAlchemy models for LogRun bot."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class DiscordUser(Base):
    """Discord user account model."""

    __tablename__ = "discord_users"

    id: mapped_column(Integer, primary_key=True)
    discord_id: mapped_column(Integer, unique=True, nullable=False)
    discord_username: mapped_column(String(255), nullable=False)
    discord_tag: mapped_column(String(255), nullable=False)
    verified: mapped_column(Integer, default=0)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class Character(Base):
    """WoW character model."""

    __tablename__ = "characters"
    __table_args__ = (UniqueConstraint("character_name", "realm", "region", name="unique_character"),)

    id: mapped_column(Integer, primary_key=True)
    discord_id: mapped_column(Integer, nullable=False)
    character_name: mapped_column(String(255), nullable=False)
    realm: mapped_column(String(255), nullable=False)
    region: mapped_column(String(10), nullable=False)
    guild: mapped_column(String(255), nullable=True)
    class_name: mapped_column(String(50), nullable=True)
    spec: mapped_column(String(50), nullable=True)
    race: mapped_column(String(50), nullable=True)
    gender: mapped_column(String(10), nullable=True)
    level: mapped_column(Integer, default=70)
    item_level: mapped_column(Integer, nullable=True)
    primary: mapped_column(Integer, default=1)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class Performance(Base):
    """Character performance data model."""

    __tablename__ = "performances"

    id: mapped_column(Integer, primary_key=True)
    character_id: mapped_column(Integer, nullable=False)
    discord_id: mapped_column(Integer, nullable=False)
    heroic_best_perf_avg: mapped_column(Float, default=0.0)
    rank_role: mapped_column(String(50), default="Member")
    refresh_count: mapped_column(Integer, default=0)
    last_refresh: mapped_column(DateTime, nullable=True)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class Guild(Base):
    """WoW guild model."""

    __tablename__ = "guilds"
    __table_args__ = (UniqueConstraint("guild_name", "realm", "region", name="unique_guild"),)

    id: mapped_column(Integer, primary_key=True)
    guild_name: mapped_column(String(255), nullable=False)
    realm: mapped_column(String(255), nullable=False)
    region: mapped_column(String(10), nullable=False)
    faction: mapped_column(String(50), nullable=True)
    member_count: mapped_column(Integer, default=0)
    total_members_verified: mapped_column(Integer, default=0)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class GuildStatistics(Base):
    """Guild statistics model."""

    __tablename__ = "guild_statistics"

    id: mapped_column(Integer, primary_key=True)
    guild_id: mapped_column(Integer, nullable=False)
    avg_performance: mapped_column(Float, default=0.0)
    raider_elite_count: mapped_column(Integer, default=0)
    raider_count: mapped_column(Integer, default=0)
    casual_count: mapped_column(Integer, default=0)
    member_count: mapped_column(Integer, default=0)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class DiscordRole(Base):
    """Discord role assignment model."""

    __tablename__ = "discord_roles"
    __table_args__ = (UniqueConstraint("guild_id", "role_type", "role_name", name="unique_discord_role"),)

    id: mapped_column(Integer, primary_key=True)
    guild_id: mapped_column(Integer, nullable=False)
    discord_role_id: mapped_column(Integer, nullable=False)
    role_name: mapped_column(String(255), nullable=False)
    role_type: mapped_column(String(50), nullable=False)  # rank, class, type, admin
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class DiscordChannel(Base):
    """Discord channel model."""

    __tablename__ = "discord_channels"
    __table_args__ = (UniqueConstraint("guild_id", "channel_name", name="unique_discord_channel"),)

    id: mapped_column(Integer, primary_key=True)
    guild_id: mapped_column(Integer, nullable=False)
    discord_channel_id: mapped_column(Integer, nullable=False)
    channel_name: mapped_column(String(255), nullable=False)
    channel_type: mapped_column(String(50), nullable=False)  # text, voice
    category_name: mapped_column(String(255), nullable=True)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    """Audit log for bot actions."""

    __tablename__ = "audit_logs"

    id: mapped_column(Integer, primary_key=True)
    action_type: mapped_column(String(100), nullable=False)
    performed_by: mapped_column(Integer, nullable=False)
    target_discord_id: mapped_column(Integer, nullable=True)
    target_character_id: mapped_column(Integer, nullable=True)
    details: mapped_column(Text, nullable=True)
    guild_id: mapped_column(Integer, nullable=False)
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class BotConfiguration(Base):
    """Bot configuration settings."""

    __tablename__ = "bot_configuration"

    id: mapped_column(Integer, primary_key=True)
    guild_id: mapped_column(Integer, unique=True, nullable=False)
    configured: mapped_column(Integer, default=0)
    prefix: mapped_column(String(10), default="!")
    log_channel_id: mapped_column(Integer, nullable=True)
    admin_role_id: mapped_column(Integer, nullable=True)
    verify_role_id: mapped_column(Integer, nullable=True)
    settings: mapped_column(Text, nullable=True)  # JSON config
    created_at: mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: mapped_column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
