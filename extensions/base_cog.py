import logging

from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot
        self.logger = logging.getLogger(f"discord.{__name__}")
