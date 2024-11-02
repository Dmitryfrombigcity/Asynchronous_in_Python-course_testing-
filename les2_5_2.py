from inspect import getgeneratorstate
from typing import Generator, Any


def echo_gen() -> Generator[Any, Any, str]:
    value = None
    while True:
        try:
            value = yield value
        except StopIteration:
            return 'StopIteration. Генератор завершил свою работу!'
        except Exception as error:
            value = f'Получено переданное исключение. Тип: {error.__class__.__name__}. Сообщение: {error.__str__()}'


g = echo_gen()

g.send(None)
print(g.send(1))
print(g.throw(ValueError("oops!")))  # выводится информация о переданном исключении и
print(g.send(2))  # генератор продолжает работать
try:
    g.throw(StopIteration)
except StopIteration as error:
    print(error)
print(getgeneratorstate(g))  # проверяем что генератор завершил работу после передачи StopIteration

# 1
# Получено переданное исключение. Тип: ValueError. Сообщение: oops!
# 2
# StopIteration. Генератор завершил свою работу!
# GEN_CLOSED
