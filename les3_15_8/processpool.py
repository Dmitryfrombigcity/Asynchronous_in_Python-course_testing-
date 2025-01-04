import asyncio
import warnings as _wr
from contextlib import asynccontextmanager
from functools import partial
from multiprocessing import get_context
from threading import Lock
from time import sleep
from typing import Any, AsyncIterator, NoReturn, Callable, Coroutine, Iterator

import pytest

from les3_15_8.processpool_extra import ProcessPoolExecutor as ProcessPoolExecutor, logger as logger

_wr.simplefilter("ignore")

################# Эмуляция #####################################

results: list[Any] = []
entities: list[Callable[[], str] | Coroutine] = []
n: int = 1


def f0() -> str:
    print('func f0 start/done\n', end='')
    logger.debug('func start/done')
    return f0.__name__


def f1() -> str:
    print('func f1 start\n', end='')
    logger.debug('func start')
    sleep(1)
    # raise TypeError("oops!")
    print('func f1 done\n', end='')
    logger.debug('func done')
    return f1.__name__


def f2() -> str:
    print('func f2 start\n', end='')
    logger.debug('func start')
    sleep(2)
    # raise TypeError("oops!")
    print('func f2 done\n', end='')
    logger.debug('func done')
    return f2.__name__


def f3() -> str:
    print('func f3 start\n', end='')
    logger.debug('func start')
    sleep(3)
    # raise TypeError("oops!")
    print('func f3 done\n', end='')
    logger.debug('func done')
    return f3.__name__


def f4() -> str:
    print('func f4 start\n', end='')
    logger.debug('func start')
    sleep(4)
    print('func f4 done\n', end='')
    logger.debug('func done')
    return f4.__name__


def f5() -> str:
    print('func f5 start\n', end='')
    logger.debug('func start')
    sleep(5)
    print('func f5 done\n', end='')
    logger.debug('func done')
    return f5.__name__


async def c0() -> str:
    print('coro c0 start/done\n', end='')
    logger.debug('coro start/done')
    return c0.__name__


async def c1() -> str:
    print('coro c1 start\n', end='')
    logger.debug('coro start')
    await asyncio.sleep(1)
    # raise TypeError("oops!")
    print('coro c1 done\n', end='')
    logger.debug('coro done')
    return c1.__name__


async def c2() -> str:
    print('coro c2 start\n', end='')
    logger.debug('coro start')
    await asyncio.sleep(2)
    # raise TypeError("oops!")
    print('coro c2 done\n', end='')
    logger.debug('coro done')
    return c2.__name__


async def c3() -> str:
    print('coro c3 start\n', end='')
    logger.debug('coro start')
    await asyncio.sleep(3)
    raise TypeError("oops!")
    print('coro c3 done\n', end='')
    logger.debug('coro done')
    return c3.__name__


#############################################################

def _show_futures(process_pool: ProcessPoolExecutor) -> list[str] | None:
    try:
        return [
            (f'{process_pool._pending_work_items[i].future} '
             f'{process_pool._pending_work_items[i].fn}')
            for i in process_pool._pending_work_items
        ]
    except BaseException as err:
        logger.info(repr(err))
    return None


def _show_queue(process_pool: ProcessPoolExecutor) -> list[str] | None:
    with lock:

        with process_pool.rlock, process_pool.wlock:
            try:
                lst: list[str] = []
                for _ in range(process_pool._call_queue.qsize()):
                    item = process_pool._call_queue.get()
                    if item:
                        lst.append(str(item.fn))
                    process_pool._call_queue.put(item)
                return lst
            except AttributeError:
                logger.info('process_pool is closed')
            except BaseException as err:
                logger.info(repr(err))

        return None


@asynccontextmanager
async def process_executor(n: int) -> AsyncIterator[ProcessPoolExecutor]:
    process_pool = ProcessPoolExecutor(max_workers=n, mp_context=context)
    sentinel = False
    try:
        yield process_pool
    except BaseException:
        sentinel = True
    finally:
        print(_show_queue(process_pool))
        print('<<TaskGroup finished>>')
        logger.info('<<TaskGroup finished>>')
        logger.debug(_show_queue(process_pool))
        logger.debug(_show_futures(process_pool))
        process_pool.shutdown(wait=True, cancel_futures=sentinel)


def cb(
        tg: asyncio.TaskGroup,
        process_pool: ProcessPoolExecutor,
        task: asyncio.Task[Any] | asyncio.Future[Any],
) -> None:
    async def temp() -> NoReturn:
        raise Exception

    if output := _show_queue(process_pool):
        print(output)

    logger.debug(f'{task}')
    if not task.cancelled():
        try:
            results.append(task.result())
        except Exception as exc:
            if type(task) is asyncio.Task and (coro_name := task.get_coro()):
                print(f"{coro_name.__name__} завершилась с ошибкой {exc!r}")
            results.append(f"Ошибка: {exc!r}")

            # отмена TaskGroup
            # tg._abort()               # не очень вариант

            try:  # получше
                tg.create_task(temp())
            except:  # на случай, если TaskGroup уже в отмене
                ...

    else:
        if type(task) is asyncio.Task and (coro_name := task.get_coro()):
            print(f"{coro_name.__name__} отменена")
        else:
            print(f"{task!r} отменена")


async def main() -> None:
    loop = asyncio.get_running_loop()
    print()
    try:
        async with process_executor(n) as process_pool, asyncio.TaskGroup() as tg:
            _cb = partial(cb, tg, process_pool)
            for task in entities:
                if asyncio.iscoroutine(task):
                    tg.create_task(task).add_done_callback(_cb)
                else:
                    if output := _show_queue(process_pool):
                        print(output)
                    logger.debug(_show_queue(process_pool))
                    loop.run_in_executor(process_pool, task).add_done_callback(_cb)
    except ExceptionGroup:
        logger.info('error occurred')
    logger.debug(_show_futures(process_pool))
    # await asyncio.sleep(10)


@pytest.fixture(autouse=True, scope='function')
def _setup() -> Iterator[None]:
    logger.info('start')
    global results, entities
    results = []
    entities = [f0, c0(), f1, c1(), f2, c2(), f3, c3(), f4, f5]
    yield
    logger.info('end')
    print(f'{results=}\n', end='')


@pytest.mark.timeout(20, method='thread')
@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_() -> None:
    await main()


lock = Lock()
context = get_context('fork')

if __name__ == '__main__':
    logger.info('start')
    entities = [f0, c0(), f1, c1(), f2, c2(), f3, c3(), f4, f5]
    asyncio.run(main())
    print(f'{results=}')
    logger.info('end')
