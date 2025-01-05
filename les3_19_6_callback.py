import asyncio
from functools import partial
from time import perf_counter
from typing import Any, Iterator, Literal

type T = dict[str, list[Any]]

queue: asyncio.Queue[Any] = asyncio.Queue()
event = asyncio.Event()

sentinel: Iterator[Any] | None = None
############################################################################

start = perf_counter()


async def scrap() -> T:
    while perf_counter() - start < 3:
        return {}
    return {'new': ['товар№1', 'товар№2', 'товар№3', 'товар№4', 'товар№5', 'extra']}


async def spider(item: Any) -> None:
    print(f'{item} is caught')


#############################################################################
async def coro_watcher() -> Iterator[Any]:
    while True:
        await asyncio.sleep(0.1)
        if goods := await scrap():
            break
    event.set()
    global sentinel
    sentinel = iter(goods['new'])
    return sentinel


async def coro_handler() -> Literal[True] | None:
    await event.wait()
    try:
        if sentinel is not None:
            item = next(sentinel)
            await spider(item)
            return True
    except StopIteration:
        ...
    return None


def callback(
        group: asyncio.TaskGroup,
        task: asyncio.Task
) -> None:
    if task.result():
        group.create_task(coro_handler())


async def main_logic() -> None:
    async with asyncio.TaskGroup() as group:
        _callback = partial(callback, group)
        group.create_task(coro_watcher())
        for _ in range(5):
            group.create_task(coro_handler()).add_done_callback(_callback)


if __name__ == '__main__':
    asyncio.run(main_logic())
