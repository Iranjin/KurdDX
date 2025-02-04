import os
import io
from typing import Optional, Tuple, Union

import discord


def attach(file: Union[str, bytes], file_name: Optional[str] = None) -> Tuple[str, discord.File]:
    """Attach a file to a discord message

    Args:
        file (Union[str, bytes]): The file to attach. Can be a file path (str) or file content (bytes).
        file_name (Optional[str], optional): The name of the file. If file is bytes, this must be specified.

    Raises:
        ValueError: If file is bytes and file_name is not specified.

    Returns:
        tuple: A tuple containing the URL of the attachment and the discord.File object.
    """
    if isinstance(file, str):
        file_name = file_name or os.path.basename(file)
        file = discord.File(file, file_name)
    elif isinstance(file, bytes):
        if not file_name:
            raise ValueError("file_name must be specified when file is bytes")
        file = discord.File(io.BytesIO(file), file_name)
    else:
        raise TypeError("file must be either a str or bytes")
    
    url = "attachment://" + file_name
    return url, file
