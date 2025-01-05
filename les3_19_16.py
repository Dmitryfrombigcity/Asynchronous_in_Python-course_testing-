import asyncio
from typing import Callable, TypeVar, Literal

_T = TypeVar('_T')


class TimeoutCondition(asyncio.Condition):

    async def wait_for(
            self,
            predicate: Callable[[], _T],
            timeout: int | float | None = None
    ) -> Literal[True] | _T:
        try:
            await asyncio.wait_for(
                super().wait_for(predicate), timeout=timeout
            )
            return True
        except asyncio.TimeoutError:
            return predicate()
