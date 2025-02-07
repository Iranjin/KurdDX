import subprocess

from discord.ext import commands

from . import exceptions
from .config import Config
from constants import *


def dev_only():
    async def predicate(ctx: commands.Context) -> bool:
        if not ctx.author.id in Config(CONFIG_FILE).load().get("developers", []):
            raise commands.CheckFailure("You are not a developer.")
        return True

    return commands.check(predicate)


def slash_command_only():
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.interaction is None:
            raise commands.CheckFailure("This command can only be used in a slash command.")
        return True

    return commands.check(predicate)


def ffmpeg_required():
    async def predicate(ctx: commands.Context) -> bool:
        try:
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except FileNotFoundError:
            pass
        
        raise exceptions.KurdDXError(exceptions.ExecutableNotFoundError("ffmpeg is not installed."))

    return commands.check(predicate)
