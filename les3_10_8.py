import asyncio
from typing import Any


async def wait_tasks(tasks: list[asyncio.Task], timeout: float | int) -> tuple[dict[str, Any], set]:
    done: set[asyncio.Task] = set()
    done_dict: dict[str, Any] = {}
    done, pending = await asyncio.wait(tasks, timeout=timeout)
    for item in done:
        if item.cancelled():
            done_dict[item.get_name()] = 'Cancelled'
        elif exp := item.exception():
            done_dict[item.get_name()] = exp
        else:
            done_dict[item.get_name()] = item.result()
    return done_dict, pending
