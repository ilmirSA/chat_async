import argparse
import asyncio
import json
import logging
import os

import aiofiles
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


async def submit_message(host: str,port, hash: str, message: str):

        reader, writer = await asyncio.open_connection(
            host, port)
        read_bytes=150
        try:
            data = await reader.read(read_bytes)
            logger.debug(data.decode())
            writer.write(f"{hash}\n".encode())
            await writer.drain()
            data = await reader.readline()
            json_data = data.decode().strip()
            logger.debug(json_data)
            if json.loads(json_data) is None:
                print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
                return
            message_clean = "".join(message).replace("\\n", "")
            writer.write(f"{message_clean}\n".encode())
            await writer.drain()
            logger.debug(message)
            writer.write("\n".encode())
            await writer.drain()
        finally:
            writer.close()


async def main():
    load_dotenv()
    host = os.getenv("host")
    port=5050

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
    parser.add_argument('message')

    args = parser.parse_args()

    await submit_message(host, port,user_cred['account_hash'], args.message)


if __name__ == '__main__':
    asyncio.run(main())
