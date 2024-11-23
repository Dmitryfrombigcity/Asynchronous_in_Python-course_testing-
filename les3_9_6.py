import asyncio
from typing import Any


async def coro_1():
    raise ValueError("some message")


async def coro_2():
    return 42


async def coro_3():
    raise asyncio.CancelledError("another message")

coroutines = [coro_1(), coro_2(), coro_3()]

all_results: dict[str, Any] = {}

def callback(task: asyncio.Task) -> None:
    key = f'Task_{task.get_coro().__name__}'
    try:
        value = task.result()
    except BaseException as err:
        value = err
    finally:
        all_results[key] = value


async def main() -> None:
    tasks: list[asyncio.Task] = []
    for coro in coroutines:
        tasks.append(asyncio.create_task(coro))
        tasks[-1].add_done_callback(callback)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
