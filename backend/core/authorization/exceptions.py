class AuthorizationError(Exception):
    """Base exception for authorization failures."""


class AuthorizationDenied(AuthorizationError):
    """Raised when a user is not authorized to perform an operation."""