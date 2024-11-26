import asyncio
from typing import Coroutine, Any


async def main(coroutine: Coroutine) -> Any:
    task = asyncio.create_task(coroutine)
    delay = await asyncio.create_task(response_limit())
    try:
        res = await asyncio.wait_for(task, delay)
    except TimeoutError:
        print('Задача отменена, превышено время ожидания!')
        res = None
    finally:
        return res
