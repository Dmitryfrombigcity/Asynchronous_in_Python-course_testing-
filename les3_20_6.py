import asyncio
from typing import Callable, Any, Awaitable


class AsyncHubHandler:
    def __init__(
            self,
            limit: int,
            coro_function: Callable[..., Awaitable[Any]],
            n_tasks: int
    ) -> None:
        self.sem = asyncio.Semaphore(limit)
        self.coro = coro_function
        self.tasks = n_tasks

    async def start_hub(self) -> None:
        async with asyncio.TaskGroup() as group:
            for i in range(self.tasks):
                group.create_task(self._coro())

    async def _coro(self) -> None:
        async with self.sem:
            await self.coro()
