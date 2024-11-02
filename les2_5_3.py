from itertools import count
from typing import TypeAlias, Generator

T: TypeAlias = int | float


def g_average() -> Generator[T, T, tuple[T, str, str]]:
    value = yield
    ind = count(1)
    average: T = 0
    while True:
        try:
            send_value = yield (average := value / next(ind))
            value += send_value
        except Exception as err:
            return average, err.__class__.__name__, err.__str__()


g = g_average()

print(g.send(None))  # type: ignore # выводит None
print(g.send(0))  # выводит 0.0
print(g.send(10))  # выводит 5.0, т.к. (0 + 10) / 2
print(g.send(20))  # выводит 10.0, т.к. (0 + 10 + 20) / 3
print(g.send(0))  # выводит 7.5
try:
    g.throw(ValueError("new_throw_msg"))
except StopIteration as err:  # здесь обрабатываем завершение генератора
    avr, err, msg = err.value
    print(avr, err, msg)  # выводит три значения через пробел: 7.5 ValueError new_throw_msg