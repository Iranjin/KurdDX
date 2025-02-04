from __future__ import annotations

import logging
import traceback

from discord.ext import commands

from utils.config import Config
from utils.common import *


class KurdDX(commands.Bot):
    config: Config

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logging.getLogger("KurdDX")

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
