"""Example module demonstrating code style and patterns.

This module shows the expected code style, including:
- Type hints for all function signatures
- Google-style docstrings
- Error handling patterns
- Validation in a stdlib dataclass

This template ships no runtime dependencies. Reach for pydantic (or attrs, or
whatever fits) when a project actually needs it — `uv add pydantic`.
"""

from dataclasses import dataclass
from typing import TypedDict

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20
MINIMUM_AGE = 18


@dataclass
class UserConfig:
    """Configuration for a user, validated on construction.

    Attributes:
        username: The user's unique username (3-20 characters, alphanumeric).
        email: The user's email address.
        age: The user's age (must be 18+).
        is_active: Whether the user account is active.
    """

    username: str
    email: str
    age: int
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate the field values.

        Raises:
            ValueError: If any field fails validation.
        """
        if not USERNAME_MIN_LENGTH <= len(self.username) <= USERNAME_MAX_LENGTH:
            msg = (
                f"Username must be {USERNAME_MIN_LENGTH}-{USERNAME_MAX_LENGTH} "
                f"characters"
            )
            raise ValueError(msg)
        if not self.username.isalnum():
            msg = "Username must contain only alphanumeric characters"
            raise ValueError(msg)
        if "@" not in self.email:
            msg = "Invalid email address"
            raise ValueError(msg)
        if self.age < MINIMUM_AGE:
            msg = f"User must be {MINIMUM_AGE} or older"
            raise ValueError(msg)


class ProcessResult(TypedDict):
    """Result type for process_data function."""

    success: bool
    data: str | None
    error: str | None


def greet_user(name: str, greeting: str = "Hello") -> str:
    """Generate a personalized greeting.

    Args:
        name: The name to greet.
        greeting: The greeting word to use (default: "Hello").

    Returns:
        A formatted greeting string.

    Example:
        >>> greet_user("Alice")
        'Hello, Alice!'
        >>> greet_user("Bob", "Hi")
        'Hi, Bob!'
    """
    return f"{greeting}, {name}!"


def process_data(data: str, validate: bool = True) -> ProcessResult:
    """Process input data with optional validation.

    Args:
        data: The data string to process.
        validate: Whether to validate the input (default: True).

    Returns:
        ProcessResult dict with success status, data, and optional error.

    Raises:
        ValueError: If validation is enabled and data is invalid.
    """
    if validate and not data.strip():
        return ProcessResult(success=False, data=None, error="Data cannot be empty")

    try:
        processed = data.strip().upper()
        return ProcessResult(success=True, data=processed, error=None)
    except Exception as e:
        return ProcessResult(success=False, data=None, error=str(e))


def calculate_stats(numbers: list[int]) -> dict[str, float]:
    """Calculate basic statistics for a list of numbers.

    Args:
        numbers: List of integers to analyze.

    Returns:
        Dictionary containing mean, min, max, and count.

    Raises:
        ValueError: If the numbers list is empty.
    """
    if not numbers:
        msg = "Cannot calculate statistics for empty list"
        raise ValueError(msg)

    return {
        "mean": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "count": len(numbers),
    }
