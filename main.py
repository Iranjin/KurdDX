import logging
import os

import discord

from utils.config import Config
from utils.exceptions import *
from kurd_dx import KurdDX
from constants import *


def main():
    logger = logging.getLogger("KurdDX.main")
    
    config = Config(CONFIG_FILE)
    try:
        config.load()
    except FileNotFoundError as e:
        logger.error("File '%s' not found!", e.filename)
        return

    token_config = Config(TOKEN_FILE)
    try:
        token_config.load()
    except FileNotFoundError as e:
        logger.error("File '%s' not found!", e.filename)
        return
    
    token = token_config.get("token")
    if token is None:
        filename = os.path.basename(token_config.path)
        raise TokenNotFoundError(f"Token not found in '{filename}'")

    intents = discord.Intents.all()
    
    bot = KurdDX(
        command_prefix = config.get("command_prefix", "!"),
        intents = intents,
    )

    bot.config = config

    bot.run(token_config.get("token"), root_logger=True)


if __name__ == "__main__":
    main()
