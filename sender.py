import asyncio
import logging

logger = logging.getLogger(__name__)


async def write_to_chat(hash: str, message: str):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)
    data = await reader.read(100)
    logger.debug(data.decode())
    writer.write(f"{hash}\n".encode())
    writer.write(f"{message}\n".encode())
    writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()


async def main():
    logging.basicConfig(level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
                        )
    await write_to_chat("98604f8e-5c77-11ef-abed-0242ac110002", "как дела ребята?")


if __name__ == '__main__':

    asyncio.run(main())
