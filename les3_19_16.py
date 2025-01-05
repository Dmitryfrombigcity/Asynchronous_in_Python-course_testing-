import asyncio
from typing import Callable, TypeVar

_T = TypeVar('_T')


class TimeoutCondition(asyncio.Condition):

    async def wait_for(
            self,
            predicate: Callable[[], _T],
            timeout: int | float | None = None
    ) -> _T:
        try:
            result = await asyncio.wait_for(
                super().wait_for(predicate), timeout=timeout
            )
        except asyncio.TimeoutError:
            result = predicate()
        return result
