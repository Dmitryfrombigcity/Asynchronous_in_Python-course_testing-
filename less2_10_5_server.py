# server
import socket
from collections import deque
from select import select
from typing import Iterator, TypeAlias

T: TypeAlias = Iterator[tuple[str, socket.socket]]


def create_server() -> T:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen()
    while True:
        yield 'accept', server_socket
        conn, addr = server_socket.accept()
        # print(f'Connection from {addr}')
        queue.append(handle_client(conn))


def handle_client(client_sock: socket.socket) -> T:
    while True:
        yield 'recv', client_sock
        data = client_sock.recv(1024)
        try:
            # print(f'socket:{client_sock.getpeername()[-1]}>> received data {data!r}')
            numbers = [int(n) for n in data.decode().split()]
            res = sum(numbers)
        except Exception as er:
            msg = repr(er)
        else:
            msg = f'{'+'.join(map(str, numbers))}={res}'
        finally:
            yield 'send', client_sock
            client_sock.send(msg.encode())


def event_loop() -> None:
    read: dict[socket.socket, T] = {}
    write: dict[socket.socket, T] = {}
    while True:
        if not queue:
            sock_for_read, sock_for_write, _ = select(read, write, [])
            for sock in sock_for_read:
                queue.append(read.pop(sock))
            for sock in sock_for_write:
                queue.append(write.pop(sock))

        task = queue.popleft()
        try:
            method, sock = next(task)
            match method:
                case 'send':
                    write[sock] = task
                case _:
                    read[sock] = task
        except socket.error:
            print(f'Потеря связи с клиентом.')


queue = deque((create_server(),))
