import asyncio
import time
from typing import Coroutine, Self, Callable, Any


class TaskGroupCB:
    def __init__(self,
                 callback: Callable[[asyncio.Task], Any]
                 ) -> None:
        self.callback = callback
        self._set: set[asyncio.Task] = set()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: None,
            exc_val: None,
            exc_tb: None
    ) -> None:
        await asyncio.gather(*self._set)

    def create_task(
            self, coro: Coroutine[None, int, int],
            *,
            name: str | None = None
    ) -> asyncio.Task:
        task = asyncio.create_task(coro, name=name)
        self._set.add(task)
        task.add_done_callback(self._set.discard)
        task.add_done_callback(self.callback)
        return task


async def coro(i: int) -> int:
    return await asyncio.sleep(i / 10, i)


def callback(task: asyncio.Task) -> None:
    print(f"Задача {task.get_name()} завершилась успешно с результатом {task.result()}")


async def main() -> None:
    async with TaskGroupCB(callback) as tgc:
        for n in range(10):
            tgc.create_task(coro(n), name=f"task#{n}")


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}с.")
