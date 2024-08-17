import argparse
import asyncio
import datetime
import os

import aiofiles
from dotenv import load_dotenv


async def save_chat(host: str, port: str, file_path: str) -> None:
    reader, writer = await asyncio.open_connection(
        host, port)
    async with aiofiles.open(file_path, 'a', encoding='UTF-8') as file:
        while True:
            try:
                data = await reader.read(100)
                now = datetime.datetime.now()
                formatted_date = now.strftime("%d.%m.%Y %H:%M")
                formatted_text = f'[{formatted_date}] {data.decode()}'
                print(formatted_text)
                await file.write(formatted_text)
            except UnicodeDecodeError:
                pass


async def main():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    file_path = os.getenv("file_path")

    parser = argparse.ArgumentParser(description="Скачивает файлы и упаковывает из в zip")
    parser.add_argument('-host', '--host',default=host)
    parser.add_argument('-port', '--port', type=str, default=port)
    parser.add_argument('-file', '--history', type=str, default=file_path)
    args = parser.parse_args()
    await save_chat(args.host, args.port, args.path)


if __name__ == '__main__':
    asyncio.run(main())
