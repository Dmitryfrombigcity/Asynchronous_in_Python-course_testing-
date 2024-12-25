# подавить warning
# [tool.pytest.ini_options]
# asyncio_default_fixture_loop_scope = "function"

import asyncio
from time import perf_counter

import pytest

pytest_plugins = ('pytest_asyncio',)


######################################################################
#                          Your code

class TimeoutLock(asyncio.Lock):
    ...


async def coro(timeout):
    ...


lock = TimeoutLock()
start = perf_counter()


######################################################################
async def cashed_request() -> None:
    print(f'{perf_counter() - start:.2f}> Задача {asyncio.current_task().get_name()} выполнила запрос')
    await asyncio.sleep(2)
    print(f'{perf_counter() - start:.2f}> Задача {asyncio.current_task().get_name()} выполнила сохранение в кэш')


@pytest.mark.parametrize("timer, times", [(2.5, 3), (0, 2), (None, 2)])
@pytest.mark.asyncio(scope="session")
async def test_main(timer, times) -> None:
    global start
    start = perf_counter()
    print()
    await asyncio.gather(*(asyncio.create_task(coro(timer), name=f'Task-{i + 1}') for i in range(times)))
