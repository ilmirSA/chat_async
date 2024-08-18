import asyncio
import logging

logger = logging.getLogger(__name__)


async def write_to_chat(hash: str, message: str):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)
    data = await reader.read(150)
    logger.debug(data.decode())
    writer.write(f"{hash}\n".encode())
    data = await reader.read(400)
    logger.debug(data.decode())
    writer.write(f"{message}\n".encode())
    logger.debug(message)
    writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()


async def main():
    logging.basicConfig(filename='sender.log',level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(levelname)1s:%(module)1s:%(message)s",
                        encoding="UTF-8"
                        )
    await write_to_chat("98604f8e-5c77-11ef-abed-0242ac110002", "Hello World?")


if __name__ == '__main__':


    asyncio.run(main())
