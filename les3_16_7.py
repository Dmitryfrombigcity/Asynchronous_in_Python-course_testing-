import asyncio
from typing import Coroutine, Self


class _Iterator:
    def __init__(self, coroutines: list[Coroutine]) -> None:
        self._tasks = {asyncio.create_task(coro) for coro in coroutines}
        self._queue: asyncio.Queue[asyncio.Task] = asyncio.Queue()
        for task in self._tasks:
            task.add_done_callback(self._queue.put_nowait)
            task.add_done_callback(self._tasks.remove)

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> asyncio.Task:
        if not self._tasks:
            raise StopAsyncIteration
        return await self._queue.get()


def async_for_completed(aws: list[Coroutine]) -> _Iterator:
    if (isinstance(aws, list) and
            all(map(asyncio.iscoroutine, aws))):
        return _Iterator(aws)
    raise TypeError("Должен быть передан список с объектами корутин")


# async def a(): ...
#
#
# def b(): ...
#
#
# c = [b]
# async_for_completed(c)
