import sys
from itertools import count
from random import randrange
from time import time, sleep, perf_counter

from loguru import logger

total_count = count(1)


class FishingRod:
    def __init__(self,
                 delay: float | int,
                 name: str = ""
                 ) -> None:
        self.name = name
        self.delay = delay

    def __repr__(self) -> str:
        return f'{self.name}  delay={self.delay}'

    def get(self) -> bool:
        if self.delay > 0:
            return True
        print(f"На удочку №{self.name} поймал одну, всего {next(total_count)}")
        return False


def main() -> None:
    n = 9
    tasks: list[tuple[float, FishingRod]] = []
    for i in range(1, n + 1):
        delay = randrange(1, 11)
        tasks.append(
            (time() + delay, FishingRod(delay=delay, name=str(i)))
        )
    tasks.sort(reverse=True)

    while tasks:
        time_mark, fishing_rod = tasks.pop()
        logger.debug(f'Popping --> {fishing_rod=}')
        wait_time = time_mark - time()
        logger.debug(f'{wait_time=:.4f}')
        if wait_time > 0:
            sleep(wait_time)
        fishing_rod.delay = time_mark - time()
        logger.debug(f'{fishing_rod.delay=:.4f}')
        state = fishing_rod.get()
        logger.debug(f'Getting --> {state= }, {fishing_rod.delay=:.4f}')
        # этого не случится никогда
        if state:
            ...


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    start_time = perf_counter()
    main()
    print(f'Затраченное время {perf_counter() - start_time:.2f}c.')
