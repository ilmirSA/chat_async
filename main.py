import asyncio
import aiofiles
import datetime


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    print("Соединение Установлено")
    async with aiofiles.open("chat_history.txt", 'a',encoding='UTF-8') as file:
        while True:
            try:
                data = await reader.read(100)
                now = datetime.datetime.now()
                formatted_date = now.strftime("%d.%m.%Y %H:%M")
                formatted_text = f'[{formatted_date}] {data.decode()}'
                print(formatted_text)
                await file.write(formatted_text)
            except (UnicodeDecodeError):
                pass


async def main():
    # asyncio.create_task(tcp_echo_client())
    await tcp_echo_client()


if __name__ == '__main__':
    asyncio.run(main())
