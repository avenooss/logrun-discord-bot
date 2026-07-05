"""Application constants."""

from enum import Enum

# Warcraft Logs Performance Tiers
PERFORMANCE_TIERS = {
    "GOD": (100, 100),
    "Raider Elite": (99, 99),
    "Raider++": (95, 98),
    "Raider+": (75, 94),
    "Casual Raider": (50, 74),
    "Casual Player": (25, 49),
    "Member": (0, 24),
}

# WoW Classes
WOW_CLASSES = [
    "Warrior",
    "Paladin",
    "Hunter",
    "Rogue",
    "Priest",
    "Death Knight",
    "Shaman",
    "Mage",
    "Warlock",
    "Monk",
    "Druid",
    "Demon Hunter",
    "Evoker",
]

# Role Types
ROLE_TYPES = ["Tank", "Healer", "DPS"]

# WoW Regions
WOW_REGIONS = {"us": "United States", "eu": "Europe", "kr": "Korea", "tw": "Taiwan", "cn": "China"}

# Discord Server Categories
CATEGORIES = {
    "Information": "Information and announcements",
    "General": "General discussion",
    "Raid": "Raid operations",
    "Logs": "Warcraft Logs integration",
    "Administration": "Officer and admin",
    "Utilities": "Bot utilities",
}

# Discord Server Channels
CHANNELS = {
    "Information": [
        ("let-start", "Welcome and getting started"),
        ("bot-guide", "Bot usage guide"),
        ("announcements", "Guild announcements"),
    ],
    "General": [("general", "General chat")],
    "Raid": [("raid-chat", "Raid discussion"), ("raid-signup", "Raid event signups")],
    "Logs": [("logs", "Raid logs and analysis")],
    "Administration": [("bot-logs", "Bot activity logs"), ("officers", "Officer-only channel")],
    "Utilities": [],
}

# Admin Roles
ADMIN_ROLES = ["Guild Master", "Officer", "Raid Leader", "Bot Manager"]

# WoW Specs
WOW_SPECS = {
    "Warrior": ["Arms", "Fury", "Protection"],
    "Paladin": ["Holy", "Protection", "Retribution"],
    "Hunter": ["Beast Mastery", "Marksmanship", "Survival"],
    "Rogue": ["Assassination", "Combat", "Subtlety"],
    "Priest": ["Discipline", "Holy", "Shadow"],
    "Death Knight": ["Blood", "Frost", "Unholy"],
    "Shaman": ["Elemental", "Enhancement", "Restoration"],
    "Mage": ["Arcane", "Fire", "Frost"],
    "Warlock": ["Affliction", "Demonology", "Destruction"],
    "Monk": ["Brewmaster", "Mistweaver", "Windwalker"],
    "Druid": ["Balance", "Feral", "Guardian", "Restoration"],
    "Demon Hunter": ["Havoc", "Vengeance"],
    "Evoker": ["Devastation", "Preservation"],
}

# Warcraft Logs API
WARCRAFT_LOGS_OAUTH_URL = "https://www.warcraftlogs.com/oauth/token"
WARCRAFT_LOGS_API_URL = "https://www.warcraftlogs.com/api/v2/client"

# Battle.net API
BATTLENET_API_BASE_URL = "https://{region}.api.blizzard.com"

# Cache keys
CACHE_KEYS = {
    "warcraft_logs_token": "wl_token",
    "character_performance": "char_perf:{character_id}",
    "guild_roster": "guild_roster:{guild_id}",
    "guild_stats": "guild_stats:{guild_id}",
    "leaderboard": "leaderboard:{guild_id}",
}

# Pagination
PAGINATION_SIZE = 10
MAX_RESULTS = 100

# Rate limits
WARCRAFT_LOGS_RATE_LIMIT = 100
BATTLENET_RATE_LIMIT = 36000


class DiscordColor(Enum):
    """Discord embed colors."""

    PRIMARY = 0x5865F2
    SUCCESS = 0x57F287
    DANGER = 0xED4245
    WARNING = 0xFAA61A
    INFO = 0x00B0F4
    PURPLE = 0x9C27B0
    GOLD = 0xFFD700


class ErrorCode(Enum):
    """Application error codes."""

    INVALID_CHARACTER = "INVALID_CHARACTER"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    API_ERROR = "API_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    UNAUTHORIZED = "UNAUTHORIZED"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
