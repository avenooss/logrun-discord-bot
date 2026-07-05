"""Custom exception classes."""

from typing import Optional


class LogRunException(Exception):
    """Base exception for LogRun bot."""

    def __init__(self, message: str, code: Optional[str] = None):
        """Initialize exception.
        
        Args:
            message: Error message
            code: Error code for logging/tracking
        """
        self.message = message
        self.code = code
        super().__init__(self.message)


class VerificationError(LogRunException):
    """Raised when character verification fails."""

    pass


class APIError(LogRunException):
    """Raised when external API call fails."""

    pass


class WarcraftLogsError(APIError):
    """Raised when Warcraft Logs API call fails."""

    pass


class BattleNetError(APIError):
    """Raised when Battle.net API call fails."""

    pass


class DatabaseError(LogRunException):
    """Raised when database operation fails."""

    pass


class CharacterNotFoundError(VerificationError):
    """Raised when character is not found."""

    pass


class InvalidInputError(LogRunException):
    """Raised when user input is invalid."""

    pass


class PermissionError(LogRunException):
    """Raised when user lacks required permissions."""

    pass


class ConfigurationError(LogRunException):
    """Raised when configuration is invalid."""

    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass
