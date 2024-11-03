from typing import Generator, Iterator, Callable


def sub_gen() -> Generator[str, None, int]:
    total_sum = 0
    for i in range(1, 5):
        total_sum += i
        yield f"+{i}, sum={total_sum}"
    return total_sum


def handler(data: int) -> None:
    print(f"callback for {data}")


def callback_delegate(
        g: Generator[str, None, int],
        func: Callable[[int], None]) -> Iterator[str]:
    value = yield from g
    func(value)


for elem in callback_delegate(sub_gen(), handler):
    print(elem)

# +1, sum=1
# +2, sum=3
# +3, sum=6
# +4, sum=10
# callback for 10
