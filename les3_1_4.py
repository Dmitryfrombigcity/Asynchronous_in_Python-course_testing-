import asyncio


def get_loop():
    loop = asyncio.get_event_loop()
    return True if loop.is_running() else False, loop

async def main():
    print(get_loop())

if __name__ == '__main__':
    print(get_loop())
    asyncio.run(main())
