import argparse
import asyncio
import datetime
import os

import aiofiles
from dotenv import load_dotenv


async def write_to_chat(hash: str, message: str):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)
    await reader.read(100)
    writer.write(f"{hash}\n".encode())
    writer.write(f"{message}\n".encode())
    writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()


async def main():
    await write_to_chat("98604f8e-5c77-11ef-abed-0242ac110002", "как дела ребята?")


if __name__ == '__main__':
    asyncio.run(main())
