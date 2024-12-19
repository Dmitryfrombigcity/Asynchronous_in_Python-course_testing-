import asyncio
from functools import partial


def my_callback(url: str, task: asyncio.Task) -> None:
    # функция использует аргумент url
    ...


async def main() -> None:
    async with asyncio.TaskGroup() as group:
        for callback, coro, arg in zip(callbacks, coroutines, arguments):
            group.create_task(coro(arg), name=coro.__name__).add_done_callback(partial(callback, arg))


if __name__ == '__main__':
    asyncio.run(main())
