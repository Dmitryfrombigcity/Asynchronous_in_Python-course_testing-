import asyncio
from typing import Coroutine


async def coro_1() -> int:
    await asyncio.sleep(1)
    return 1


async def response_limit() -> float:
    await asyncio.sleep(0)
    return 3.5


async def coro_3() -> int:
    await asyncio.sleep(3)
    return 3


async def coro_4() -> int:
    await asyncio.sleep(4)
    return 4


coroutines = [coro_1(), coro_3(), response_limit(), coro_4()]


async def main(coroutines: list[Coroutine]) -> list[str]:
    tasks: list[asyncio.Task] = []
    try:
        async with asyncio.timeout(None) as atm:
            for coro in coroutines:
                locals()[f'task_{coro.__name__}'] = asyncio.create_task(coro)
                tasks.append(locals()[f'task_{coro.__name__}'])
            delay = await locals()['task_response_limit']
            atm.reschedule(asyncio.get_running_loop().time() + delay)
            await asyncio.gather(*tasks)
    except TimeoutError:
        ...
    res = [coro_name for task in tasks
           if (coro_name := task.get_coro().__name__) != 'response_limit' and not task.cancelled()]
    return res


if __name__ == '__main__':
    print(asyncio.run(main(coroutines)))
