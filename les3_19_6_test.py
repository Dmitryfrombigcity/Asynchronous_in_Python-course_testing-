import asyncio
from time import perf_counter
from typing import Any

type T = dict[str, list[Any]]

start = perf_counter()


async def scrap() -> T:
    while perf_counter() - start < 3:
        return {}
    return {'new': ["товар№1", "товар№2", "товар№3", "товар№4", "товар№5"]}


async def spider(item: Any) -> None:
    print(f'{item} is caught')


#########################Your code #####################################

async def coro_watcher() -> None:
    ...


async def coro_handler() -> None:
    ...


async def main_logic() -> None:
    ...


if __name__ == '__main__':
    asyncio.run(main_logic())
