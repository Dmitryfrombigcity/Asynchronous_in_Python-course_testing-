import asyncio


async def s():
    for symbol in "abc":
        await asyncio.sleep(0)
        print(symbol)


async def m():
    for symbol in "АБВГДЕ":
        await asyncio.sleep(0)
        print(symbol)
    raise ValueError("Ё, wtf?")


async def xl():
    for n in range(10, 16):
        await asyncio.sleep(0)
        print(n)


async def main():
    task_1 = asyncio.create_task(s())
    task_2 = asyncio.create_task(m())
    task_3 = asyncio.create_task(xl())
    await task_1
    try:
        await task_2
    except ValueError:
        ...
    await task_3


if __name__ == "__main__":
    asyncio.run(main())
