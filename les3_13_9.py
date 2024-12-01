import asyncio
from concurrent.futures.thread import ThreadPoolExecutor


def a():
    ...


async def b():
    ...


entities = [a, b()]


async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=len(entities)) as executer:
        await asyncio.gather(
            *(item if asyncio.iscoroutine(item) else loop.run_in_executor(executer, item) for item in entities)
        )


if __name__ == '__main__':
    asyncio.run(main())
