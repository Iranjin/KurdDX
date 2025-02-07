import logging
import io

from discord.ext import commands, tasks

from utils import predicates
from utils.exceptions import *
from console.register_commands import register_commands
from kurd_dx import KurdDX
from base_cog import BaseCog


class KurdDX_EXT(BaseCog):
    async def on_init(self):
        self.update_presence.start()
        self.bot.before_invoke(self.check_maintenance)
    
    @tasks.loop(minutes=10)
    async def update_presence(self):
        activity = discord.Game(name=f"{len(self.bot.guilds)} servers")
        status = discord.Status.online

        config = self.bot.config
        config.load()
        
        is_maintenance = config.get("maintenance", False)

        if is_maintenance:
            activity = discord.Game(name="Maintenance")
            status = discord.Status.do_not_disturb
        
        await self.bot.change_presence(activity=activity, status=status)
    
    async def check_maintenance(self, ctx: commands.Context):
        cs_command = self.bot.get_command("cs")
        if cs_command and ctx.command == cs_command:
            return
        
        config = self.bot.config
        config.load()

        is_dev = ctx.author.id in config.get("developers", [])
        is_maintenance = config.get("maintenance", False)
        
        if is_maintenance and not is_dev:
            raise KurdDXError(MaintenanceError())

    @commands.command("cs")
    @predicates.dev_only()
    async def cs_command(self, ctx: commands.Context, *, command: str):
        logger = logging.getLogger("discord.dev_command")
        logger.setLevel(logging.INFO)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        async with ctx.typing():
            console = register_commands()
            await console.execute_command(self.bot, command)

            log_contents = log_stream.getvalue() or "No output"
            content = f"```{log_contents}```"
            
            if len(content) > 2000:
                await ctx.message.reply(file=discord.File(io.StringIO(log_contents), filename="log.txt"), mention_author=False)
            else:
                await ctx.message.reply(content, mention_author=False)

    @commands.command("csx")
    @predicates.dev_only()
    async def csx_command(self, ctx: commands.Context, *, command: str):
        logger = logging.getLogger("discord.dev_command")
        logger.setLevel(logging.INFO)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        
        formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)

        async with ctx.typing():
            console = register_commands()
            await console.execute_command(self.bot, command)

            log_contents = log_stream.getvalue() or "No output"
            content = f"```{log_contents}```"
            
            if len(content) > 2000:
                await ctx.message.reply(file=discord.File(io.StringIO(log_contents), filename="log.txt"), mention_author=False)
            else:
                await ctx.message.reply(content, mention_author=False)
    
    @commands.command("csf")
    @predicates.dev_only()
    async def csf_command(self, ctx: commands.Context, *, command: str):
        logger = logging.getLogger("discord.dev_command")
        logger.setLevel(logging.INFO)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        async with ctx.typing():
            console = register_commands()
            await console.execute_command(self.bot, command)

            log_contents = log_stream.getvalue() or None
            
            if log_contents is None:
                await ctx.send("No output")
                return
            
            await ctx.message.reply(file=discord.File(io.StringIO(log_contents), filename="log.txt"), mention_author=False)

    @commands.command("csfx")
    @predicates.dev_only()
    async def csfx_command(self, ctx: commands.Context, *, command: str):
        logger = logging.getLogger("discord.dev_command")
        logger.setLevel(logging.INFO)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        
        formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)

        async with ctx.typing():
            console = register_commands()
            await console.execute_command(self.bot, command)

            log_contents = log_stream.getvalue() or None
            
            if log_contents is None:
                await ctx.send("No output")
                return

            await ctx.message.reply(file=discord.File(io.StringIO(log_contents), filename="log.txt"), mention_author=False)


async def setup(bot: KurdDX):
    await bot.add_cog(KurdDX_EXT(bot))
