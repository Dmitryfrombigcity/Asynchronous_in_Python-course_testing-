# Не корректная работа семафора после отмены acquire()
import asyncio
import time


async def coro(sema: asyncio.Semaphore):
    try:
        await asyncio.wait_for(sema.acquire(), timeout=1)
    except TimeoutError:
        pass

    await asyncio.sleep(1)
    sema.release()


async def main():
    semaphore = asyncio.Semaphore(2)
    await asyncio.gather(*(coro(semaphore) for _ in range(8)))
    await asyncio.gather(*(coro(semaphore) for _ in range(8)))


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Выполнилась за {time.perf_counter() - start_time:.2f}с.")
