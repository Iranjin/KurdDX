from __future__ import annotations

import traceback
import logging
import sys

from discord.ext import commands

from utils.config import Config
from utils.common import *
from console.register_commands import register_commands


class KurdDX(commands.Bot):
    config: Config

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logging.getLogger("KurdDX.bot")

    async def setup_hook(self):
        self.loop.create_task(self.dev_console())
    
    async def dev_console(self):
        console = register_commands()

        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, input)

            sys.stdout.write("\033[A\033[K")
            sys.stdout.flush()

            try:
                await console.execute_command(self, command)
            except commands.ExtensionFailed:
                self.logger.error("Failed to execute command")
                self.logger.error("A restart is required to apply changes")
            except Exception as e:
                self.logger.error(f"Command execution failed: {e}")

    async def on_ready(self):
        self.logger.info("Logged in as %s", self.user)

        await self.load_all_extensions()

        await self.tree.sync()

    async def load_all_extensions(self):
        for path in get_extension():
            if path in self.extensions:
                continue
            try:
                await self.load_extension(path)
            except Exception as e:
                tb = traceback.format_exc()
                self.logger.error(f"Failed to load extension {path}: {e}\n{tb}")
            else:
                self.logger.info(f"Loaded extension {path}")
        
        if not self.extensions:
            self.logger.warning("No extensions loaded")
