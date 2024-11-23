import asyncio
from asyncio import TaskGroup
from typing import Coroutine
#
#
# class AlarmOverheatException(Exception):
#     ...
#
#
# async def service_diag() -> None:
#     await asyncio.sleep(3)
#     raise AlarmOverheatException()
#
#
# async def coro_1() -> None:
#     await asyncio.sleep(4)
#     raise ValueError("some message")
#
#
# async def coro_2() -> int:
#     return 42
#
#
# async def coro_3() -> int:
#     return 34
#
#
# coroutines = [coro_1(), coro_2(), coro_3()]


async def main(coros: list[Coroutine]) -> None:
    try:
        async with TaskGroup() as group:
            group.create_task(service_diag())
            for coro in coros:
                group.create_task(coro)
    except ExceptionGroup as err_group:
        for err in err_group.exceptions:
            if isinstance(err, AlarmOverheatException):
                print("WARNING: Критическая нагрузка, текущие задачи группы отменены!")
            else:
                print(err)


# if __name__ == "__main__":
#     asyncio.run(main(coroutines))
