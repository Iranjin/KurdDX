from __future__ import annotations

from typing import TypeVar, Generic
import inspect

import discord
from discord.ext import commands
from discord.app_commands.errors import AppCommandError


T = TypeVar('T')


class KurdDXError(commands.CommandError, Generic[T]):
    """
    Base error class for the KurdDX bot.

    This class is used to represent general errors that occur within the bot.
    It wraps the original AppCommandError and provides more detailed information.

    Attributes:
        original (T): The original error that occurred.
    """
    original: T

    def __init__(self, original: T) -> None:
        self.original = original
        super().__init__(str(original))


class OutOfRangeError(AppCommandError):
    """
    Error raised when a value is out of range.

    This error occurs when the bot attempts to use a value that is outside
    the specified range (e.g. a number that is too small or too large).

    Attributes:
        value (int): The value that is out of range.
        min_value (int): The minimum value allowed.
        max_value (int): The maximum value allowed.

    Args:
        value (int): The value that is out of range.
        min_value (int): The minimum value allowed.
        max_value (int): The maximum value allowed.
        message (Optional[str]): The error message to display.
    """
    value: int
    min_value: int
    max_value: int
    
    def __init__(self, value: int, min_value: int, max_value: int, message: str | None = None) -> None:
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        
        frame = inspect.currentframe()
        if frame is None:
            raise ValueError("No current frame found")
        
        frame = frame.f_back
        if frame is None:
            raise ValueError("No previous frame found")
        
        var_name = next(
            name
            for name, val in frame.f_locals.items()
            if val == value
        )

        if message is not None:
            message = message.format(value=value, min_value=min_value, max_value=max_value)
        else:
            if value < min_value:
                message = f"`{var_name}` must be at least `{min_value}`"
            elif value > max_value:
                message = f"`{var_name}` must be at most `{max_value}`"
        
        super().__init__(message)


class InvalidSubcommandError(AppCommandError):
    """
    Error raised when an invalid subcommand is invoked.

    This error occurs when the bot attempts to execute a subcommand that does
    not exist within the parent command group.
    """
    group: discord.app_commands.Group
    given_subcommand_name: str | None
    
    def __init__(self, group: discord.app_commands.Group, given_subcommand_name: str | None = None) -> None:
        self.group = group
        self.given_subcommand_name = given_subcommand_name
        super().__init__("Invalid subcommand")


class TokenNotFoundError(AppCommandError):
    """
    Error raised when a required token is not found.

    This error occurs when the bot attempts to access a specific token
    that does not exist or is unavailable.
    """
    pass


class ResourceNotFoundError(AppCommandError):
    """
    Error raised when a requested resource is not found.

    This error occurs when the bot attempts to access a specific resource
    (such as a file or data) that does not exist.
    """
    pass


class ExecutableNotFoundError(AppCommandError):
    """
    Error raised when an executable file is not found.

    This error occurs when the bot attempts to execute a specific file
    (such as a command or script) that cannot be found.
    """
    pass


class LibraryNotFoundError(AppCommandError):
    """
    Error raised when a required library is not found.

    This error occurs when the bot attempts to import a specific library
    that is not installed on the system.
    """
    pass


class MaintenanceError(AppCommandError):
    """
    Error raised when the bot is under maintenance.

    This error occurs when the bot is in maintenance mode and certain
    commands are restricted to developers only.
    """
    message: str
    
    def __init__(self, message: str | None = None) -> None:
        self.message = message or "Bot is under maintenance"
        super().__init__(self.message)
