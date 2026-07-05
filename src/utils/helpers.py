"""Helper utility functions."""

from datetime import datetime, timezone
from typing import Optional


def get_timestamp() -> datetime:
    """Get current UTC timestamp.
    
    Returns:
        Current datetime in UTC
    """
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object.
    
    Args:
        dt: Datetime object to format
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    if not dt:
        return "Unknown"
    return dt.strftime(format_str)


def calculate_percentile_tier(performance: float) -> str:
    """Calculate performance tier from percentile.
    
    Args:
        performance: Performance percentile (0-100)
        
    Returns:
        Performance tier name
    """
    if performance >= 100:
        return "GOD"
    elif performance >= 99:
        return "Raider Elite"
    elif performance >= 95:
        return "Raider++"
    elif performance >= 75:
        return "Raider+"
    elif performance >= 50:
        return "Casual Raider"
    elif performance >= 25:
        return "Casual Player"
    else:
        return "Member"


def format_large_number(num: int) -> str:
    """Format large numbers with commas.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted number string
    """
    return f"{num:,}"


def truncate_string(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate string to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def get_ordinal_suffix(number: int) -> str:
    """Get ordinal suffix for number (1st, 2nd, 3rd, etc).
    
    Args:
        number: Number to get suffix for
        
    Returns:
        Number with ordinal suffix
    """
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"
