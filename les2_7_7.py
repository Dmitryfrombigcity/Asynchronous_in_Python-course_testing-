import select
from typing import Iterable, Tuple, Any, IO


def check_ready_to(
        files_for_read: Iterable[IO[Any]],
        files_for_write: Iterable[IO[Any]],
        timeout: int = 0
) -> Tuple[bool, bool, bool]:
    try:
        ready_for_read, ready_for_write, _ = select.select(
            files_for_read, files_for_write, [], timeout
        )
    except (TypeError, ValueError):
        return False, False, False
    return (
        True if ready_for_read else False,
        True if ready_for_write else False,
        True if timeout else False
    )


# if __name__ == '__main__':
#     notest: IO[Any] = ...
#     with open('test_2') as test_2:
#         ...
#     with open('test') as test:
#         print(check_ready_to([test, test_2], [], 3))
