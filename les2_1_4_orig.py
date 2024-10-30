import heapq
import sys
from itertools import count
from random import randrange
from time import time, sleep, perf_counter

from loguru import logger

total_count = count(1)


class FishingRod:
    def __init__(self, delay: float | int, name: str = ""):
        self.name = name
        self.delay = delay

    def __repr__(self) -> str:
        return f'{self.name}  delay={self.delay:.4f}'

    def get(self):
        if self.delay > 0:
            return True, self.delay
        logger.info(f"На удочку №{self.name} поймал одну, всего {next(total_count)}")
        return False, None


def main():
    n = 9
    tasks = []
    for i in range(1, n + 1):
        delay = randrange(1, 21)
        tasks.append((time() + delay, i, FishingRod(delay=delay, name=str(i))))
    heapq.heapify(tasks)  # формируем кучу из списка задач, чтобы затем всегда брать самую приоритетную удочку

    while tasks:
        time_mark, _id, fishing_rod = heapq.heappop(tasks)  # берем задачу, получаем самую приоретную
        logger.debug(f'Pop out from a heap --> {fishing_rod=}')
        wait_time = time_mark - time()  # считаем время необходимого ожидания
        logger.debug(f'Calculate --> {wait_time=:.4f}')
        if wait_time > 0:
            sleep(wait_time)
        state, delay = fishing_rod.get()  # смотрим на удочку, проверяем ее
        logger.debug(f'Get from FishingRod --> {state= }, {fishing_rod.delay=:.4f}')
        fishing_rod.delay -= time() - time_mark  # обновляем время ожидания, отнимаем уже потраченное
        # откладываем задачу обратно в список задач, если время еще не пришло, клева пока нет.
        logger.debug(f'Set new {fishing_rod.delay=:.4f}')
        if state:
            heapq.heappush(tasks, (time() - time_mark, _id, fishing_rod))
            logger.debug(f'Push back into a heap--> {fishing_rod=}')
        else:
            logger.debug(f'--> {fishing_rod=} --> is gone')


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    start_time = perf_counter()
    main()
    logger.info(f'Затраченное время {perf_counter() - start_time:.2f}c.')
