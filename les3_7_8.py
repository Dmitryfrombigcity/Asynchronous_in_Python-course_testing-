import asyncio
from asyncio import TaskGroup, CancelledError, Future  # noqa
from typing import Any


async def coro_1() -> str:
    await asyncio.sleep(2)
    return "first"


async def coro_2() -> str:
    raise Exception
    return "second"


async def coro_3() -> str:
    await asyncio.sleep(2)
    return "third"


coroutines = [coro_1(), coro_2(), coro_3()]


# async def main() -> None:
#     tasks = []
#     global res
#     for coro in coroutines:
#         tasks.append(asyncio.create_task(coro))
#         tasks[-1].add_done_callback(callback)
#     try:
#         res = asyncio.gather(*tasks, return_exceptions=True)
#         await res
#     except CancelledError:
#         ...


async def main() -> None:
    try:
        async with TaskGroup() as group:
            tasks = []
            for coro in coroutines:
                tasks.append(group.create_task(coro))
                tasks[-1].add_done_callback(callback)
    except ExceptionGroup:
        ...


def callback(task: asyncio.Task) -> None:
    if not task.cancelled():
        if temp := task.exception():
            results.append(temp)
            # # asyncio.gather
            # if res is not None:
            #     res.cancel()
        else:
            results.append(task.result())
    else:
        cancelled.append(task.get_coro().__name__)


if __name__ == "__main__":
    # asyncio.gather
    # res: Future | None = None
    cancelled: list[str] = []
    results: list[Any | Exception] = []
    asyncio.run(main())

