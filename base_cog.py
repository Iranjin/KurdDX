import logging
import asyncio

from discord.ext import commands

from kurd_dx import KurdDX


class BaseCog(commands.Cog):
    def __init__(self, bot: KurdDX):
        super().__init__()

        self.bot = bot
        self.logger = logging.getLogger(f"KurdDX.ext.{self.__class__.__name__}")

        self.bot.loop.create_task(self._init_wrapper())

    async def _init_wrapper(self):
        if asyncio.iscoroutinefunction(self.on_init):
            await self.on_init()
        else:
            self.on_init()

    def on_init(self):
        pass
