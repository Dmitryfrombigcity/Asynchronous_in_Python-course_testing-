import asyncio
from typing import Awaitable, Iterable


# async def coro_1() -> None:
#     raise ValueError('opa')
#
#
# async def coro_2() -> int:
#     await asyncio.sleep(1)
#     return 2
#
#
# async def coro_3() -> int:
#     await asyncio.sleep(3)
#     return 3
#
# async def coro_4() -> int:
#     await asyncio.sleep(4)
#     return 4
#
#
# aws = [coro_1(), coro_2(), coro_3(), coro_4()]


async def main(aws: Iterable[Awaitable], *, timeout: int | float | None = None) -> None:
    for aw in asyncio.as_completed(aws, timeout=timeout):
        try:
            result = await aw
        except Exception as err:
            if isinstance(err, TimeoutError):
                result = 'Завершение по таймауту!'
                break
            else:
                result = err
        finally:
            print(result)


# if __name__ == '__main__':
#     asyncio.run(main(aws, timeout=5))
