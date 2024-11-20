import asyncio
from asyncio import TaskGroup
from typing import Any


async def coro_1() -> str:
    await asyncio.sleep(1)
    return "first"


async def coro_2() -> str:
    raise Exception
    return "second"


async def coro_3() -> str:
    await asyncio.sleep(1)
    return "third"


coroutines = [coro_1(), coro_2(), coro_3()]


async def main() -> None:
    try:
        async with TaskGroup() as group:
            temp = asyncio.create_task(coroutines[-1])
            temp.add_done_callback(callback)
            for coro in coroutines[:-1]:
                group.create_task(coro).add_done_callback(callback)
    except ExceptionGroup:
        ...
    finally:
        await temp


def callback(task: asyncio.Task) -> None:
    if not task.cancelled():
        if temp := task.exception():
            results.append(temp)
        else:
            results.append(task.result())
    else:
        cancelled.append(task.get_coro().__name__)


if __name__ == "__main__":
    cancelled: list[str] = []
    results: list[Any | Exception] = []
    asyncio.run(main())
    # print(results, cancelled)
