import asyncio
from asyncio import TaskGroup
from functools import partial
from typing import AsyncIterator, Any, Never


async def json_gen() -> AsyncIterator[int]:
    item = iter(range(1, 11))
    while True:
        try:
            yield next(item)
        except StopIteration:
            break


async def registrator(elem: int) -> None:
    print(f'{elem} зарегистрирован для дальнейшей обработки')


def final() -> None:
    print('Final')


#####################################################################

def callback(
        group: asyncio.TaskGroup,
        fut: asyncio.Task[Any]
) -> None:

    async def _close_group() -> Never:
        raise BaseException

    group.create_task(_close_group())


async def producer(
        queue: asyncio.LifoQueue[Any]
) -> None:
    async for elem in json_gen():
        await queue.put(elem)
    await queue.join()


async def consumer(
        queue: asyncio.LifoQueue[Any]
) -> None:
    while True:
        elem = await queue.get()
        await registrator(elem)
        queue.task_done()


async def producer_consumer(
        queue: asyncio.LifoQueue[Any]
) -> None:
    try:
        async with TaskGroup() as group:
            task = group.create_task(producer(queue))
            _callback = partial(callback, group)
            task.add_done_callback(_callback)
            for _ in (1, 2):
                group.create_task(consumer(queue))
    except BaseException:
        final()


if __name__ == '__main__':
    queue: asyncio.LifoQueue[Any] = asyncio.LifoQueue()
    asyncio.run(producer_consumer(queue))
    print('End')
