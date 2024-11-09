import select
import socket
from typing import Callable, List


def idle_select(sockets: List[socket.socket],
                idle_handler: Callable[[], None],
                timeout: int | float
                ) -> List[socket.socket]:
    sentinel, _, _ = select.select(sockets, [], [], timeout)
    if not sentinel:
        idle_handler()
    return sentinel
