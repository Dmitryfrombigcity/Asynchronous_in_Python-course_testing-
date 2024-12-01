import asyncio

from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any


def a():
    ...


async def b():
    ...


entities = [a, b()]


async def main() -> list[Any]:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=len(entities)) as executer:
        res: list[Any] = []
        for item in asyncio.as_completed(
                item if asyncio.iscoroutine(item) else loop.run_in_executor(executer, item) for item in entities
        ):
            res.append(await item)
    return res


if __name__ == '__main__':
    print(asyncio.run(main()))
