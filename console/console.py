import logging
import shlex
from typing import Callable, Optional, Tuple, Dict, List, Any

from discord.ext import commands


logger = logging.getLogger("discord.console")


class CsCommand:
    def __init__(self, name: str):
        self.name = name
        self.arguments: Dict[str, Tuple[type, Optional[Any]]] = {}
        self.function: Optional[Callable[..., Any]] = None

    def add_argument(self, name: str, type: type, default: Optional[Any] = None):
        self.arguments[name] = (type, default)

    def set_function(self, function: Callable[..., Any]):
        self.function = function

    async def execute(self, bot: commands.Bot, args: List[str]) -> Any:
        if len(args) > len(self.arguments):
            raise ValueError(f"Expected at most {len(self.arguments)} arguments but got {len(args)}.")

        parsed_args = {}
        for (name, (type, default)), value in zip(self.arguments.items(), args):
            try:
                if type == bool:
                    if value.lower() in ["true", "yes", "1"]:
                        parsed_args[name] = True
                    elif value.lower() in ["false", "no", "0"]:
                        parsed_args[name] = False
                    else:
                        raise ValueError(f"Argument '{name}' must be of type {type.__name__}.")
                else:
                    parsed_args[name] = type(value)
            except ValueError:
                raise ValueError(f"Argument '{name}' must be of type {type.__name__}.")

        for name, (type, default) in self.arguments.items():
            if name not in parsed_args:
                if default is not None:
                    parsed_args[name] = default
                else:
                    raise ValueError(f"Argument '{name}' is required but not provided.")

        if self.function:
            return await self.function(bot, **parsed_args)


class Cs:
    __commands: Dict[str, CsCommand]

    def __init__(self):
        self.__commands = {}

    def get_commands(self) -> Dict[str, CsCommand]:
        return self.__commands

    def add_command(self, command: CsCommand):
        self.__commands[command.name] = command
    
    def remove_command(self, command_name: str):
        del self.__commands[command_name]

    async def execute_command(self, bot: commands.Bot, command_string: str) -> Any:
        command_name: Optional[str] = None
        args: List[str] = []

        for name in sorted(self.__commands.keys(), key=len, reverse=True):
            if command_string.startswith(name):
                command_name = name
                args = shlex.split(command_string[len(name):].strip())
                break

        if command_name and command_name in self.__commands:
            logger.info(f"> {command_name} {' '.join(args)}")
            return await self.__commands[command_name].execute(bot, args)
        else:
            raise ValueError(f"Command '{command_string}' not found.")
