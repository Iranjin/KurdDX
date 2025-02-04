import discord
from discord.ext import commands

from utils import local_file
from .base_cog import BaseCog


class TemplateExt(BaseCog):
    @commands.Cog.listener("on_message")
    async def on_message_event(self, message: discord.Message):
        self.logger.info("%s > %s", message.author, message.content)
    
    @commands.Cog.listener("on_guild_join")
    async def on_guild_join_event(self, guild: discord.Guild):
        self.logger.info("Joined guild %s (%d)", guild.name, guild.id)

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove_event(self, guild: discord.Guild):
        self.logger.info("Left guild %s (%d)", guild.name, guild.id)

    @commands.hybrid_command("ping", description="Checks the bot's latency to the Discord server.")
    async def ping_command(self, ctx: commands.Context):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        await ctx.send(f"Pong! `{ping}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(TemplateExt(bot))
