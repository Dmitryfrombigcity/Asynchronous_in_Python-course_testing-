import asyncio

import pytest

from semaphore_3_13 import Semaphore as SEM


class Semaphore(SEM):
    def __init__(self, value: int = 1) -> None:
        self._value_init = value
        self.sentinel = 0
        super().__init__(value=value)

    def __setattr__(self, key: str, value: int) -> None:
        """fix release"""

        if key == '_value':
            if value > self._value_init:
                value = self._value_init
        return object.__setattr__(self, key, value)

    @property
    def value(self) -> int:
        return self._value_init

    @value.setter
    def value(self, value: int) -> None:
        if value <= 0:
            print("Semaphore value must be > 0")
            return
        temp = self._value_init - value
        self._value_init = value

        # Adjusting the current semaphore value
        if temp > 0:
            self.sentinel = temp
        else:
            for _ in range(-temp):
                self.release()

    def release(self) -> None:
        while self.sentinel:
            self.sentinel -= 1
            return
        super().release()

    def __str__(self) -> str:
        """ waiters[all/not_done/cancelled]"""

        extra = 'locked' if self.locked() else f'unlocked, value:{self._value}'
        if self._waiters:
            not_done = len([w for w in (self._waiters or ()) if not w.done()])
            cancelled = len([w for w in (self._waiters or ()) if w.cancelled()])
            extra = (
                f'{extra}, '
                f'waiters:{len(self._waiters)}/{not_done}/{cancelled},'
                f' value:{self._value}'
            )
        return f'<Semaphore [{extra}]>'


async def coro(
        sem: Semaphore,
        timeout: int,
) -> None:
    print(
        'before>',
        asyncio.current_task().get_name() if asyncio.current_task() else None,
        sem
    )
    try:
        await asyncio.wait_for(sem.acquire(), timeout=timeout)
    except TimeoutError:
        pass
    await asyncio.sleep(1)
    sem.release()
    print(
        '>after',
        asyncio.current_task().get_name() if asyncio.current_task() else None,
        sem
    )


async def coro_2(
        sem: Semaphore,
        limit: int,
        start_value: int
) -> None:
    async with sem:
        print(f'Current {sem.value=}')
        await asyncio.sleep(1)

    # Condition
    threshold = len([w for w in (sem._waiters or ()) if not w.done()])
    if sem._waiters and (threshold > limit / 2):
        sem.value = sem.value + 1 if sem.value + 1 < start_value * 3 \
            else start_value * 3
    else:
        sem.value = sem.value - 1 if sem.value > start_value \
            else start_value
    print(
        asyncio.current_task().get_name() if asyncio.current_task() else None,
        sem
    )


@pytest.mark.parametrize('sem, timeout', [(2, 1), (2, None)])
@pytest.mark.asyncio
async def test_1(sem: int, timeout: int) -> None:
    print()
    semaphore = Semaphore(sem)
    print('First round')
    await asyncio.gather(*(coro(semaphore, i) for i in range(1, 7)),
                         coro(semaphore, timeout))
    print('Second round')
    await asyncio.gather(*(coro(semaphore, i) for i in range(1, 7)))


@pytest.mark.parametrize('sem,limit', [(-1, 10), (2, 0), (2, 30), (3, 50), (5, 100)])
@pytest.mark.asyncio
async def test_2(sem: int, limit: int) -> None:
    print()
    semaphore = Semaphore(sem)
    await asyncio.gather(*(coro_2(semaphore, limit, sem) for _ in range(limit)))
