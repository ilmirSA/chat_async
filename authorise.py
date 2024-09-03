import argparse
import asyncio
import logging
import os

import aiofiles
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

logging.basicConfig(filename='auth.log', level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="%(levelname)1s:%(module)1s:%(message)s",
                    encoding="UTF-8"
                    )


async def authorise(host: str,port:int, username: str) -> None:
    reader, writer = await asyncio.open_connection(
        host, port)
    try:
        data = await reader.readline()

        logger.debug(data.decode())
        writer.write("\n".encode())
        await writer.drain()
        data = await reader.readline()
        logger.debug(data.decode())
        writer.write(str(username).encode())
        await writer.drain()
        writer.write("\n".encode())
        await writer.drain()
        data = await reader.readline()
        logger.debug(data.decode())
        json_data = data.decode().strip()

        async with aiofiles.open('cred.txt', 'w') as file:
            await file.write(json_data)
    finally:
        writer.close()


async def main():
    logging.basicConfig(filename='auth.log', level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(levelname)1s:%(module)1s:%(message)s",
                        encoding="UTF-8"
                        )

    load_dotenv()
    host = os.getenv("host")
    port = 5050
    parser = argparse.ArgumentParser(description="Регестрирует пользоватлея")
    parser.add_argument('-u', '--username', help="Напишите юзернейм")
    args = parser.parse_args()
    await authorise(host,port, args.username)


if __name__ == '__main__':
    asyncio.run(main())
