import asyncio
import logging

import aiofiles

logger = logging.getLogger(__name__)

logging.basicConfig(filename='auth.log', level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="%(levelname)1s:%(module)1s:%(message)s",
                    encoding="UTF-8"
                    )

async def authorise(host: str, username: str) -> None:
    reader, writer = await asyncio.open_connection(
        host, 5050)
    data = await reader.readline()

    logger.debug(data.decode())
    writer.write("\n".encode())
    data = await reader.readline()
    logger.debug(data.decode())
    writer.write(str(username).encode())
    writer.write("\n".encode())
    data = await reader.readline()
    logger.debug(data.decode())
    json_data = data.decode().strip()

    async with aiofiles.open('cred.txt', 'w') as file:
        await file.write(json_data)
    writer.close()
    await writer.wait_closed()

