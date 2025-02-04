from __future__ import annotations

import os
import re
import asyncio
from typing import Generator, TypeVar, AsyncIterator, Callable, Any

import discord


T = TypeVar("T")


async def run_in_async(func: Callable[..., T], *args: Any) -> T:
    """
    Run a synchronous function in an asynchronous context.

    Args:
        func (Callable[..., T]): The synchronous function to run.
        *args (Any): Arguments to pass to the function.

    Returns:
        T: The result of the function.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)


async def async_to_list(iterable: AsyncIterator[T]) -> list[T]:
    """
    Convert an asynchronous iterator to a list.

    Args:
        iterable (AsyncIterator[T]): The asynchronous iterator to convert.

    Returns:
        list[T]: A list containing all items from the asynchronous iterator.
    """
    return [item async for item in iterable]


async def get_webhook(
    channel: discord.TextChannel,
    name: str | None = None,
    reason: str | None = None
) -> discord.Webhook:
    """
    Retrieves an existing webhook from the given channel or creates one if none exist.

    Parameters
    ----------
    channel : discord.TextChannel
        The text channel from which to retrieve or create a webhook.
    name : str | None, optional
        The name of the webhook. Defaults to the bot's name.
    reason : str | None, optional
        The reason for creating the webhook, if necessary.

    Returns
    -------
    discord.Webhook
        The found or newly created webhook.

    Raises
    ------
    discord.app_commands.BotMissingPermissions
        Raised if the bot lacks the `manage_webhooks` permission.
    """
    if not channel.permissions_for(channel.guild.me).manage_webhooks:
        raise discord.app_commands.BotMissingPermissions(["manage_webhooks"])

    name = name or channel.guild.me.name
    reason = reason or "Webhook created for automated tasks by the bot"

    webhook = discord.utils.get(await channel.webhooks(), name=name)

    return webhook or await channel.create_webhook(name=name, reason=reason)


def get_avatar(user: discord.User) -> discord.Asset:
    """
    Returns the avatar of a user, falling back to the default avatar.

    Parameters
    ----------
    user : discord.User
        The user whose avatar to retrieve.

    Returns
    -------
    discord.Asset
        The user's avatar or default avatar.
    """
    return user.avatar or user.default_avatar


def truncate(string: str, max_length: int, ellipsis: str | None = "...") -> str:
    """
    Truncates a string to a maximum length, appending an ellipsis if needed.

    Parameters
    ----------
    string : str
        The string to truncate.
    max_length : int
        The maximum allowed length of the string.
    ellipsis : str | None, optional
        The string to append when truncating. Defaults to "...".

    Returns
    -------
    str
        The truncated string.
    """
    return string if len(string) <= max_length else string[:max_length - len(ellipsis if ellipsis else "")] + (ellipsis or "")


def get_extension() -> Generator[str, None, None]:
    """
    Yields the names of Python files from the 'extension' directory that define an async setup function.

    Yields
    ------
    str
        The names of valid extension files containing async setup function.
    """
    EXTENSION_DIR = "extensions"
    async_setup_pattern = re.compile(r'^\s*async\s+def\s+setup\s*\(', re.MULTILINE)

    for path in os.listdir(EXTENSION_DIR):
        if path.startswith("_") or not path.endswith(".py"):
            continue

        full_path = os.path.join(EXTENSION_DIR, path)

        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if async_setup_pattern.search(content):
                name, _ = os.path.splitext(full_path)
                yield name.replace(os.sep, os.extsep)
