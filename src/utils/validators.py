"""Input validation utilities."""

import re
from typing import Optional

from src.config.constants import WOW_CLASSES, WOW_REGIONS


def validate_character_name(name: str) -> bool:
    """Validate WoW character name.
    
    Args:
        name: Character name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) < 2 or len(name) > 12:
        return False
    return bool(re.match(r"^[a-zA-Z]+$", name))


def validate_realm_name(realm: str) -> bool:
    """Validate WoW realm name.
    
    Args:
        realm: Realm name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not realm or len(realm) < 2 or len(realm) > 50:
        return False
    return bool(re.match(r"^[a-zA-Z0-9\s'-]+$", realm))


def validate_class(class_name: str) -> bool:
    """Validate WoW class.
    
    Args:
        class_name: Class name to validate
        
    Returns:
        True if valid, False otherwise
    """
    return class_name in WOW_CLASSES


def validate_region(region: str) -> bool:
    """Validate WoW region.
    
    Args:
        region: Region code to validate
        
    Returns:
        True if valid, False otherwise
    """
    return region.lower() in WOW_REGIONS


def validate_performance(performance: float) -> bool:
    """Validate performance percentile.
    
    Args:
        performance: Performance value to validate
        
    Returns:
        True if valid, False otherwise
    """
    return 0 <= performance <= 100


def validate_discord_id(user_id: int) -> bool:
    """Validate Discord user ID.
    
    Args:
        user_id: Discord user ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(user_id, int) and user_id > 0


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove potentially dangerous characters
    text = text.strip()
    text = re.sub(r"[<>@#&`]", "", text)
    
    # Truncate to max length
    if len(text) > max_length:
        text = text[:max_length].rstrip()
    
    return text
