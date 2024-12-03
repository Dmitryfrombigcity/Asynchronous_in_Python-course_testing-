import asyncio
import time
from types import TracebackType
from typing import Self


class AsyncDelay:
    def __init__(self, delay: float):
        self.delay = delay

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> bool | None:
        await asyncio.sleep(self.delay)
        if exc_type:
            print(f'{exc_type.__name__}: {exc_val}')
        return True


async def coro() -> None:
    print("1")
    await asyncio.sleep(0)
    print("2")
    await asyncio.sleep(1)
    print("3")
    await asyncio.sleep(2)
    print("4")


async def main() -> None:
    task = asyncio.create_task(coro())
    async with AsyncDelay(1.5):
        raise ValueError("message error!")


if __name__ == '__main__':
    _start_time = time.perf_counter()
    asyncio.run(main())
    print(f"All done in {time.perf_counter() - _start_time:.1f}c.")
