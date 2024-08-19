import asyncio
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='sender.log', level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="%(levelname)1s:%(module)1s:%(message)s",
                    encoding="UTF-8"
                    )


async def submit_message(host: str, hash: str, message: str):
    reader, writer = await asyncio.open_connection(
        host, 5050)

    data = await reader.read(150)
    logger.debug(data.decode())
    writer.write(f"{hash}\n".encode())
    data = await reader.readline()
    json_data = data.decode().strip()
    logger.debug(json_data)

    if json.loads(json_data) is None:
        writer.close()
        await writer.wait_closed()
        print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        return
    message_clean = " ".join(message).replace("\\n", "")

    writer.write(f"{message_clean}\n".encode())
    logger.debug(message)
    writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()
