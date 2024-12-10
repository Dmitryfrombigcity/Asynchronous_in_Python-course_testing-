import asyncio
from typing import Any

AsyncQueueType = asyncio.Queue[Any] | asyncio.LifoQueue[Any] | asyncio.PriorityQueue[Any]


async def producer(queue: AsyncQueueType) -> None:
    assert asyncio.current_task()
    task_name = asyncio.current_task().get_name()
    async for item in json_gen():
        try:
            async with asyncio.timeout(0.4):
                put_item = asyncio.create_task(queue.put(item))
                await asyncio.shield(put_item)
        except TimeoutError:
            print('Очередь переполнена, требуется больше потребителей!')
            await asyncio.sleep(0)
            print(queue.qsize())
            await put_item
        finally:
            print(f'{task_name} поместил {repr(item)} в очередь')
