"""Errors used in this library."""


class InvalidAuthError(Exception):
    """Raised when API returns a code indicating invalid credentials."""

    pass

class InvalidPermissionsError(Exception):
    """Raised when API returns a code indicating not enough permissions."""

    pass
