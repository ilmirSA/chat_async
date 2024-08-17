import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        try:
            data = await reader.read(100)
            print(data.decode())
        except (UnicodeDecodeError):
            pass


async def main():
    await tcp_echo_client()


if __name__ == '__main__':
    asyncio.run(main())
