from discord.ext import commands

from utils.exceptions import *
from kurd_dx import KurdDX
from base_cog import BaseCog


class Misc_EXT(BaseCog):
    @commands.hybrid_command(name="ping", description="Returns Pong!")
    async def ping(self, ctx: commands.Context):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        await ctx.send(f"Pong! `{ping}`")


async def setup(bot: KurdDX):
    await bot.add_cog(Misc_EXT(bot))
