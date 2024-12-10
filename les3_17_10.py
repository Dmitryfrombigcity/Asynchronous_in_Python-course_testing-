import asyncio
from typing import Any

AsyncQueueType = asyncio.Queue[Any] | asyncio.LifoQueue[Any] | asyncio.PriorityQueue[Any]


async def consumer(queue: AsyncQueueType) -> None:
    assert asyncio.current_task()
    task_name = asyncio.current_task().get_name()
    try:
        while True:
            async with asyncio.timeout(0.2):
                item = await queue.get()
                print(f'{task_name} извлек элемент очереди {repr(item)}')
    except TimeoutError:
        print(f'Работа {task_name} завершена!')
