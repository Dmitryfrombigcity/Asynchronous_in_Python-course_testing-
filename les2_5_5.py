from inspect import getgeneratorstate
from typing import TypeAlias, Generator, Any

T: TypeAlias = int | float


def pow_gen() -> Generator[T, Any, None]:
    value: T = 0
    while True:
        try:
            value = yield value
            value **= 2
        except Exception:
            value = 0
        except GeneratorExit:
            print('Generator pow_gen was closed!')
            raise




# сначала проверим завершение используя close в пользовательском коде
g = pow_gen()
next(g)
print(g.send(2))
print(g.send("A"))
print(g.send(1))
g.close()  # должно быть выведено сообщение согласно заданию
print(getgeneratorstate(g))  # генератор должен быть закрыт

# затем проверим, что сообщение о завершении будет выведено и при вызове close сборщиком мусора
g = pow_gen()
next(g)
print(g.send("B"))
print(g.send(3))

# 4
# 0
# 1
# Generator pow_gen was closed!
# GEN_CLOSED
# 0
# 9
# Generator pow_gen was closed!
