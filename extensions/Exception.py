from typing import Union, overload

import discord
from discord.ext import commands

from utils import exceptions, local_file
from kurd_dx import KurdDX
from base_cog import BaseCog


class Exception_EXT(BaseCog):
    @staticmethod
    async def reply(ctx: commands.Context, *args, **kwargs) -> discord.Message:
        await ctx.reply(*args, **kwargs, mention_author=False)
    
    @commands.Cog.listener("on_command_error")
    async def on_command_error_event(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.errors.CommandOnCooldown):
            return await self.on_command_cooldown_error(ctx, error)
        
        if ctx.command is not None:
            ctx.command.reset_cooldown(ctx)
        
        if isinstance(error, exceptions.KurdDXError): # NOTE: KurdDXError (util/exceptions.py)
            if isinstance(error.original, exceptions.ResourceNotFoundError):
                return await self.on_resource_not_found_error(ctx, error.original)
            elif isinstance(error.original, exceptions.ExecutableNotFoundError):
                return await self.on_executable_not_found_error(ctx, error.original)
            elif isinstance(error.original, exceptions.MaintenanceError):
                return await self.on_maintenance_error(ctx, error.original)
            elif isinstance(error.original, exceptions.OutOfRangeError):
                return await self.on_out_of_range_error(ctx, error.original)
            elif isinstance(error.original, exceptions.InvalidSubcommandError):
                return await self.on_invalid_subcommand_error(ctx, error.original)
            
        elif isinstance(error, commands.errors.HybridCommandError): # NOTE: HybridCommandError
            if isinstance(error.original, discord.app_commands.TransformerError):
                return await self.on_transformer_error(ctx, error.original)
        
        elif isinstance(error, commands.MissingPermissions):
            return await self.on_permission_error(ctx, error)
        elif isinstance(error, commands.CheckFailure):
            return await self.on_check_failure_error(ctx, error)
        elif isinstance(error, commands.BadArgument):
            return await self.on_bad_argument_error(ctx, error)
        elif isinstance(error, commands.errors.CommandInvokeError):
            return await self.on_command_invoke_error(ctx, error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await self.on_missing_required_argument_error(ctx, error)
        elif isinstance(error, commands.errors.MissingRequiredAttachment):
            return await self.on_missing_required_attachment_error(ctx, error)
        elif isinstance(error, commands.CommandNotFound):
            return # NOTE: Ignore

        await self.on_unexpected_error(ctx, error)
        raise error
    
    async def on_transformer_error(self, ctx: commands.Context, error: discord.app_commands.TransformerError):
        embed = discord.Embed(
            title="Transformer Error",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_permission_error(self, ctx: commands.Context, error: Union[commands.MissingPermissions, commands.BotMissingPermissions]):
        if isinstance(error, commands.MissingPermissions):
            message = "You are missing the following permissions"
        elif isinstance(error, commands.BotMissingPermissions):
            message = "I am missing the following permissions"
        else:
            raise ValueError(f"Invalid error type: {type(error)}")
        
        message += f"```{', '.join(error.missing_permissions)}```"

        embed = discord.Embed(
            title="Permission Error",
            description=message,
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/permission.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)

    async def on_check_failure_error(self, ctx: commands.Context, error: commands.CheckFailure):
        embed = discord.Embed(
            title="Check Failure",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)

    async def on_bad_argument_error(self, ctx: commands.Context, error: commands.BadArgument):
        embed = discord.Embed(
            title="Argument Error",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)

    async def on_command_cooldown_error(self, ctx: commands.Context, error: commands.CommandOnCooldown):
        cooldown_seconds = int(error.retry_after)

        days, remainder = divmod(cooldown_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        cooldown_time = ""
        if days > 0:    cooldown_time += f"{days} days "
        if hours > 0:   cooldown_time += f"{hours} hours "
        if minutes > 0: cooldown_time += f"{minutes} minutes "
        if seconds > 0: cooldown_time += f"{seconds} seconds "
        if cooldown_time == "": cooldown_time = "0 seconds"
        cooldown_time = cooldown_time.rstrip()

        embed = discord.Embed(
            title="Command is on cooldown",
            description=f"Please try again in `{cooldown_time}`",
            color=discord.Color.teal()
        )
        await self.reply(ctx, embed=embed)
    
    async def on_command_invoke_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        if isinstance(error.original, ValueError):
            return await self.on_value_error(ctx, error.original)
    
    async def on_value_error(self, ctx: commands.Context, error: ValueError):
        embed = discord.Embed(
            title="Value Error",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_missing_required_argument_error(self, ctx: commands.Context, error: commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Required Argument",
            description=str(error),
            color=discord.Color.teal()
        )
        embed.add_field(
            name="Usage",
            value=f"```{ctx.prefix}{ctx.command.name} {ctx.command.signature}```"
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)

    async def on_missing_required_attachment_error(self, ctx: commands.Context, error: commands.errors.MissingRequiredAttachment):
        embed = discord.Embed(
            title="Missing Required Attachment",
            description=str(error),
            color=discord.Color.teal()
        )
        embed.add_field(
            name="Usage",
            value=f"```{ctx.prefix}{ctx.command.name} {ctx.command.signature}```"
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_resource_not_found_error(self, ctx: commands.Context, error: exceptions.ResourceNotFoundError):
        embed = discord.Embed(
            title="Resource Not Found",
            description=str(error),
            color=discord.Color.teal()
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Report", style=discord.ButtonStyle.red, custom_id="button_report"))
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_executable_not_found_error(self, ctx: commands.Context, error: exceptions.ExecutableNotFoundError):
        embed = discord.Embed(
            title="Executable Not Found",
            description=str(error),
            color=discord.Color.teal()
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Report", style=discord.ButtonStyle.red, custom_id="button_report"))
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_maintenance_error(self, ctx: commands.Context, error: exceptions.MaintenanceError):
        embed = discord.Embed(
            title="Maintenance",
            description=str(error),
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/maintenance.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_out_of_range_error(self, ctx: commands.Context, error: exceptions.OutOfRangeError):
        embed = discord.Embed(
            title="Out of Range",
            description=str(error),
            color=discord.Color.teal()
        )
        embed.add_field(name="Value", value=f"```{error.value}```", inline=False)
        embed.add_field(name="Minimum Value", value=f"```{error.min_value}```", inline=False)
        embed.add_field(name="Maximum Value", value=f"```{error.max_value}```", inline=False)
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_invalid_subcommand_error(self, ctx: commands.Context, error: exceptions.InvalidSubcommandError):
        if error.given_subcommand_name is None:
            description = f"{error.group.name} group must have a subcommand"
        else:
            description = f"{error.group.name} group does not have a subcommand named `{error.given_subcommand_name}`"

        embed = discord.Embed(
            title="Invalid Subcommand",
            description=description,
            color=discord.Color.teal()
        )
        url, file = local_file.attach("res/error.png")
        embed.set_thumbnail(url=url)
        await self.reply(ctx, embed=embed, file=file)
    
    async def on_unexpected_error(self, ctx: commands.Context, error: Exception):
        embed = discord.Embed(
            title="Unexpected Error",
            color=discord.Color.teal()
        )

        name = ""
        error_ = error
        count = 0
        while hasattr(error_, "original"):
            if count > 0:
                name += " -> "
            error_ = error_.original
            name += error_.__class__.__name__
            count += 1
        
        error_string = str(error_)
        if not error_string:
            error_string = "No error message"
        
        embed.add_field(name=name, value=f"```{error_string}```", inline=False)
        embed.add_field(name="Stack Trace", value=f"```{error_.__traceback__}```", inline=False)

        url, file = local_file.attach("res/unexpected_error.png")
        embed.set_thumbnail(url=url)
     
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Report", style=discord.ButtonStyle.red, custom_id="button_report"))
        await self.reply(ctx, embed=embed, view=view, file=file)


async def setup(bot: KurdDX):
    await bot.add_cog(Exception_EXT(bot))