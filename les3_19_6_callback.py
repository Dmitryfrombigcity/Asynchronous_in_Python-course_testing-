import asyncio
from time import perf_counter
from typing import Any

type T = dict[str, list[Any]]

queue: asyncio.Queue[Any] = asyncio.Queue()

sentinel = object()
# #############################################################################
# start = perf_counter()
#
#
# async def scrap() -> T:
#     while perf_counter() - start < 3:
#         return {}
#     return {'new': ["товар№1", "товар№2", "товар№3", "товар№4", "товар№5"]}
#
#
# async def spider(item: Any) -> None:
#     print(f'{item} is caught')
#
#
# ##############################################################################
async def coro_watcher() -> T:
    while True:
        await asyncio.sleep(0.1)
        if goods := await scrap():
            break
    return goods


def callback(task: asyncio.Task) -> None:
    for item in task.result()['new']:
        queue.put_nowait(item)
    queue.put_nowait(sentinel)


async def coro_handler() -> None:
    item = await queue.get()
    if item is not sentinel:
        await spider(item)
    else:
        await queue.put(sentinel)


async def main_logic() -> None:
    async with asyncio.TaskGroup() as group:
        group.create_task(coro_watcher()).add_done_callback(callback)
        for _ in range(5):
            group.create_task(coro_handler())
#
#
# if __name__ == '__main__':
#     asyncio.run(main_logic())
