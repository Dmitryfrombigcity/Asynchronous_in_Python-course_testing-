import asyncio
import collections
from time import perf_counter
from typing import Literal, Self

type T = int | float | None


class TimeoutLock(asyncio.Lock):

    def __init__(self) -> None:
        self._timeout: T = None
        super().__init__()

    async def acquire(self, timeout: T = None) -> Literal[True]:
        if timeout is not None:
            self._timeout = timeout
        if (
                not self._locked and (self._waiters is None or
                                      all(w.cancelled() for w in self._waiters))
        ):
            self._locked = True
            return True

        if self._waiters is None:
            self._waiters = collections.deque()
        fut = self._get_loop().create_future()
        self._waiters.append(fut)
        try:
            try:
                await asyncio.wait_for(fut, self._timeout)
            except asyncio.exceptions.TimeoutError:
                self._timeout = None
            finally:
                self._waiters.remove(fut)
        except asyncio.exceptions.CancelledError:
            if not self._locked:
                self._wake_up_first()
            raise
        self._locked = True
        return True

    def release(self) -> None:
        if self._locked:
            super().release()

    def __call__(self, timeout: T) -> Self:
        if timeout is not None:
            self._timeout = timeout
        return self


lock = TimeoutLock()


async def coro(timeout: T = None) -> None:
    await lock.acquire(timeout=timeout)
    try:
        await cashed_request()
    finally:
        lock.release()


async def coro_m(timeout: T = None) -> None:
    async with lock(timeout):
        await cashed_request()


######################################################################
async def cashed_request() -> None:
    print(f'{perf_counter() - start:.2f}> Задача {asyncio.current_task().get_name()} выполнила запрос')
    await asyncio.sleep(2)
    print(f'{perf_counter() - start:.2f}> Задача {asyncio.current_task().get_name()} выполнила сохранение в кэш')


async def main() -> None:
    await asyncio.gather(*(coro_m(6) for _ in range(4)))


if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
