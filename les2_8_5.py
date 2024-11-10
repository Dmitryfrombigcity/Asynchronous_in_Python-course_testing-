import socket
from selectors import DefaultSelector
from typing import Callable, List


def idle_selectors(sockets: List[socket.socket],
                   idle_handler: Callable[[], None],
                   timeout: int | float
                   ) -> List[socket.socket]:
    with DefaultSelector() as sel:
        for sock in sockets:
            sel.register(sock, 1)
        if not (temp := sel.select(timeout=timeout)):
            idle_handler()
        return [item.fileobj for item, _ in temp]
