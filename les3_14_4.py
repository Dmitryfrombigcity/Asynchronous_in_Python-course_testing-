import asyncio
import functools
from asyncio import iscoroutine
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any


# def a() -> str:
#     return a.__name__
#
#
# async def b() -> str:
#     return b.__name__
#
#
# def c() -> None:
#     raise ValueError
#
#
# entities = [a, b(), c]


def callback(
        prefix: str,
        fut: asyncio.Task[Any] | asyncio.Future[Any]
) -> None:
    try:
        res = fut.result()
    except Exception as err:
        res = repr(err)
    finally:
        print(f'{prefix} завершена с результатом {res}\n', end='')


async def main() -> None:
    loop = asyncio.get_running_loop()
    with (
        ProcessPoolExecutor() as p_executor,
        ThreadPoolExecutor() as t_executor
    ):
        lst: list[asyncio.Task[Any] | asyncio.Future[Any]] = []
        for item in entities:
            if iscoroutine(item):
                fut = asyncio.create_task(item)
                prefix = 'Корутина'
            elif hasattr(item, 'cpu'):
                fut = loop.run_in_executor(p_executor, item)
                prefix = 'Расчетная задача'
            else:
                fut = loop.run_in_executor(t_executor, item)
                prefix = 'Блокирующая задача'
            _callback = functools.partial(callback, prefix)
            fut.add_done_callback(_callback)
            lst.append(fut)

        await asyncio.gather(*lst, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
