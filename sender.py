import argparse
import asyncio
import json
import logging
import os

import aiofiles
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


async def write_to_chat(host: str, auth_port: str, hash: str, message: str):
    reader, writer = await asyncio.open_connection(
        host, auth_port)

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

    writer.write(f"{message}\n".encode())
    logger.debug(message)
    writer.write("\n".encode())
    writer.close()
    await writer.wait_closed()


async def main():
    load_dotenv()
    host = os.getenv("host")
    auth_port = os.getenv("auth_port")

    if os.path.exists(".cred.txt"):
        print("Нету файла с авторизациями ! запустите файл authorise.py и зарегистрируйтесь")
        return
    async with aiofiles.open("cred.txt", "r") as file:
        user_cred_json = await file.read()

    user_cred = json.loads(user_cred_json)

    logging.basicConfig(filename='sender.log', level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(levelname)1s:%(module)1s:%(message)s",
                        encoding="UTF-8"
                        )

    parser = argparse.ArgumentParser(description="Отправляет сообщение  в чат")
    parser.add_argument('-m', '--message', )

    args = parser.parse_args()

    await write_to_chat(host, auth_port, user_cred['account_hash'], args.message)


if __name__ == '__main__':
    asyncio.run(main())
