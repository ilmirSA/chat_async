import argparse
import asyncio
import logging
import os

import aiofiles
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


async def user_authorize(host: str, auth_port: str, username: str) -> None:
    reader, writer = await asyncio.open_connection(
        host, auth_port)
    data = await reader.readline()

    logger.debug(data.decode())
    writer.write("\n".encode())
    data = await reader.readline()
    logger.debug(data.decode())
    writer.write(username.encode())
    writer.write("\n".encode())
    data = await reader.readline()
    logger.debug(data.decode())
    json_data = data.decode().strip()

    async with aiofiles.open('cred.txt', 'w') as file:
        await file.write(json_data)
    writer.close()
    await writer.wait_closed()


async def main():
    logging.basicConfig(filename='auth.log', level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(levelname)1s:%(module)1s:%(message)s",
                        encoding="UTF-8"
                        )

    load_dotenv()
    host = os.getenv("host")
    auth_port = os.getenv("auth_port")

    parser = argparse.ArgumentParser(description="Регестрирует пользоватлея")
    parser.add_argument('-u', '--username', help="Напишите юзернейм")
    args = parser.parse_args()
    await user_authorize(host, auth_port, args.username)


if __name__ == '__main__':
    asyncio.run(main())
