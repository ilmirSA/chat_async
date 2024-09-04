import argparse
import asyncio
import datetime
import logging
import os

import aiofiles
from dotenv import load_dotenv


async def save_chat(host: str, port: str, file_path: str) -> None:
    reader, writer = await asyncio.open_connection(
        host, port)
    read_bytes = 100
    try:
        while True:
            data = await reader.read(read_bytes)
            now = datetime.datetime.now()
            formatted_date = now.strftime("%d.%m.%Y %H:%M")
            formatted_text = f'[{formatted_date}] {data.decode()}'
            print(formatted_text)
            async with aiofiles.open(file_path, 'a', encoding='UTF-8') as file:
                await file.write(formatted_text)

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
    user_token = os.getenv("user_token")
    username = os.getenv("username")
    port = os.getenv("port")
    file_path = os.getenv("file_path")

    parser = argparse.ArgumentParser(description="Подключается к чату и сохраняет переписку ")
    parser.add_argument('-host', '--host', default=host)
    # parser.add_argument('-m','--message',nargs='+',required=True, help="Текст сообщения")
    parser.add_argument('-token', '--token', default=user_token, help="Укажите свой токен")
    parser.add_argument('-user', '--username', default=username, help="Укажите свой юзер нейм")
    parser.add_argument('-port', '--port', type=str, default=port)
    parser.add_argument('-path', '--history', type=str, default=file_path)
    args = parser.parse_args()
    await asyncio.create_task(save_chat(args.host, args.port, args.history))


if __name__ == '__main__':
    asyncio.run(main())
