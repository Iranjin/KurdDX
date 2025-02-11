import logging
import asyncio
from typing import Any

import discord

from utils import local_file
from utils.exceptions import *
from kurd_dx import KurdDX


class BaseView(discord.ui.View):
    def __init__(
        self,
        bot: KurdDX,
        timeout: float | None = 180,
        *args,
        **kwargs
    ):
        super().__init__(timeout=timeout)

        self.bot = bot
        self.__args, self.__kwargs = args, kwargs

        self.message: discord.Message | None = None

        self.logger = logging.getLogger(f"KurdDX.view.{self.__class__.__name__}")

        self.bot.loop.create_task(self._init_wrapper())

    async def _init_wrapper(self):
        if asyncio.iscoroutinefunction(self.on_init):
            await self.on_init(*self.__args, **self.__kwargs)
        else:
            self.on_init(*self.__args, **self.__kwargs)

    def on_init(self, *args, **kwargs):
        pass
    
    async def on_timeout(self):
        if self.message is None:
            return
        
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        
        await self.message.edit(view=self)

    async def send(self, ctx_inter: commands.Context | discord.Interaction, reply: bool = False, *args, **kwargs):
        if isinstance(ctx_inter, commands.Context):
            if reply:
                self.message = await ctx_inter.reply(view=self, *args, **kwargs)
            else:
                self.message = await ctx_inter.send(view=self, *args, **kwargs)
        elif isinstance(ctx_inter, discord.Interaction):
            self.message = await ctx_inter.response.send_message(view=self, *args, **kwargs)
        else:
            raise ValueError("ctx_inter must be an instance of commands.Context or discord.Interaction")
        
    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any], /):
        if isinstance(error, ValueError):
            await self.on_value_error(interaction, error)
        else:
            await super().on_error(interaction, error, item)
    
    async def on_value_error(self, interaction: discord.Interaction, error: Exception):
        embed = discord.Embed(
            title="Value Error",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/images/error.png")
        embed.set_thumbnail(url=url)
        await interaction.response.send_message(embed=embed, file=file)
