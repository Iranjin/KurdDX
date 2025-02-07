import logging
import platform
import asyncio
import os
import io

import discord
from discord.ext import commands

from utils.common import *
from utils.config import Config


logger = logging.getLogger("discord.dev_command")


discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)
discord_log_stream = io.StringIO()
formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler(discord_log_stream)
handler.setFormatter(formatter)
discord_logger.addHandler(handler)


async def say(bot: commands.Bot, channel_id: int, message_content: str) -> int:
    channel = bot.get_channel(channel_id)
    if channel is None:
        logger.error(f"Channel with ID {channel_id} not found.")
        return 1
    
    if hasattr(channel, "send"):
        await channel.send(message_content)
        logger.info(f"Sent message to channel {channel_id}: {message_content}")
    else:
        logger.error(f"Channel with ID {channel_id} is not a text channel.")
        return 1

    return 0


async def export_log(bot: commands.Bot) -> int:
    log_contents = discord_log_stream.getvalue() or None
    if log_contents is None:
        logger.error("No output")
        return 1
    else:
        log_contents = "\n".join(f"- {line}" for line in log_contents.splitlines())
    logger.info(log_contents)

    return 0


async def servers(bot: commands.Bot) -> int:
    servers = len(bot.guilds)
    
    logger.info(f"Bot is in {servers} servers")

    return 0


async def create_invite(bot: commands.Bot, guild_id: int) -> int:
    guild = bot.get_guild(guild_id)
    if guild is None:
        logger.error(f"Guild with ID {guild_id} not found.")
        return 1

    channel = None
    for c in guild.text_channels:
        if c.permissions_for(guild.me).create_instant_invite:
            channel = c
            break
    
    if channel is None:
        logger.error(f"No channel found to create invite in guild {guild.name}")
        return 1
    
    invite = await channel.create_invite()
    
    logger.info(f"Created invite for guild {guild.name}: {invite.url}")

    return 0


async def server_info(bot: commands.Bot, guild_id: int, show_members: bool) -> int:
    guild = bot.get_guild(guild_id)
    if guild is None:
        logger.error("Guild with ID %d not found.", guild_id)
        return 1
    
    logger.info("Server info for %s (%d):", guild.name, guild.id)
    logger.info("- Owner: %s (%d)",
        getattr(guild.owner, "name", "Unknown"),
        getattr(guild.owner, "id", "Unknown")
    )
    if not show_members:
        logger.info("- Members: %d", len(guild.members))
    logger.info("- Channels: %d", len(guild.channels))
    logger.info("- Roles: %d", len(guild.roles))
    logger.info("- Emojis: %d", len(guild.emojis))

    if guild.me.guild_permissions.manage_guild:
        try:
            invites = await asyncio.wait_for(guild.invites(), timeout=10)
        except asyncio.TimeoutError:
            logger.error("Failed to fetch invites in time")
        else:
            if invites != []:
                invite: discord.Invite = max(invites, key=lambda i: i.uses or -1)
                logger.info("- Invite: discord.gg/%s (%d uses)", invite.code, invite.uses)

    members = list(guild.members)

    if show_members and members:
        members.sort(key=lambda m: (m.bot, m.name))
        
        logger.info("Members (%d):", len(guild.members))

        for member in members:
            logger.info("- %s (%d)%s", member.name, member.id, " [BOT]" if member.bot else "")
    
    return 0


async def server_list(bot: commands.Bot, fetch_invite: bool) -> int:
    servers = bot.guilds
    
    if not servers:
        logger.error("Bot is not in any servers.")
        return 1

    logger.info("Server list:")

    for server in servers:
        line = f"- {server.name} ({server.id})"

        if fetch_invite:
            line += ": "
            invites = await server.invites()

            if invites:
                invite: discord.Invite = max(invites, key=lambda i: i.uses or -1)
                line += f"{invite.code} ({invite.uses} uses)"
            else:
                line += "No invites found"
        
        logger.info(line)
    
    return 0


async def reload(bot: commands.Bot, sync_tree: bool) -> int:
    logger.info("Reloading extensions")

    extensions = list(get_extension())

    for extension in extensions:
        if extension in bot.extensions:
            await bot.reload_extension(extension)
        else:
            await bot.load_extension(extension)
        
        for ext in bot.extensions:
            if ext not in extensions:
                await bot.unload_extension(ext)

        logger.info(f"Reloaded extension {extension}")
    
    if sync_tree:
        await sync(bot)
    
    logger.info("Successfully reloaded extensions")

    return 0


async def sync(bot: commands.Bot) -> int:
    await bot.tree.sync()

    logger.info("Synced tree")

    return 0


async def clear(bot: commands.Bot) -> int:
    discord_log_stream.seek(0)
    discord_log_stream.truncate()
    
    pf = platform.system()
    if pf == "Windows":
        os.system("cls")
    elif pf == "Darwin":
        os.system("clear")
    else:
        logger.error(f"Platform {pf} not supported")
        return 1

    logger.info("Cleared console")

    return 0


async def leave(bot: commands.Bot, guild_id: int) -> int:
    guild = bot.get_guild(guild_id)
    if guild is None:
        logger.error(f"Guild with ID {guild_id} not found.")
        return 1
    
    await guild.leave()
    
    logger.info(f"Left guild {guild_id}")

    return 0


async def maintenance(bot: commands.Bot, status: bool) -> int:
    logger.info(f"Setting maintenance status to {status}")
    
    config = Config("config.json").load()
    config.set("maintenance", status)

    logger.info("Successfully set maintenance status")

    await reload(bot, False)

    logger.info(f"Set maintenance status to {status}")

    return 0


async def stop(bot: commands.Bot) -> int:
    logger.info("Stopping bot...")

    await bot.close()

    return 0
