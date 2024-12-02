import asyncio
import threading
import time
from time import perf_counter


def blocking(i: int) -> None:
    print(
        f">Function_{i} started\n", end=""
    )
    time.sleep(i * 60)
    print(
        f">>Function_{i} finished "

        f"in {perf_counter() - start:.0f} sec., "
        f"the end of threads {threading.enumerate()[-1]}\n", end=""
    )


async def main() -> None:
    _, pending = await asyncio.wait(
        (
            asyncio.create_task(asyncio.to_thread(blocking, i)) for i in range(1, 30)
        ), timeout=60)

    # Scheduled in executor
    queue = asyncio.get_running_loop()._default_executor._work_queue
    print(f'{queue.qsize()=}\n', end='')

    # for item in pending:
    #     item.cancel()

    await asyncio.sleep(60)

    print(f'{queue.qsize()=}\n', end='')

    print(f">>Main coro finished "
          f"in {perf_counter() - start:.0f} sec. "
          )


if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    print(
        f">>Thread {threading.current_thread().name} is finishing "
        f" {perf_counter() - start:.0f} sec.\n", end=""
    )
