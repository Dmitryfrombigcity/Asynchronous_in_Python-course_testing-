# server
import random
import selectors
import socket
from time import sleep
from typing import Any


def create_server(address: tuple[str, int]) -> socket.socket:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen()
    return server_socket


def handler(data: bytes) -> bytes:
    try:
        print(f"received data {data!r}")
        numbers = [int(n) for n in data.decode().split()]
        res = sum(numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        sleep(random.randint(0, 3))
        return msg.encode()


def accept_conn(server_sock: socket.socket, sel: selectors.DefaultSelector) -> None:
    try:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
    except socket.error as error:
        print(f"Error accepting connection: {error}")
    else:
        sel.register(conn, 1, data=send_response)


def send_response(client_sock: socket.socket, *args: Any) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, 1, data=accept_conn)
        while True:
            if lst := sel.select(timeout=2):
                for sel_key, _ in lst:
                    sock: socket.socket = sel_key.fileobj  # type: ignore
                    callback = sel_key.data
                    try:
                        callback(sock, sel)
                    except socket.error as error:
                        print(f"Error receiving data: {error}")
                        sock.close()
                        sel.unregister(sock)
            else:
                print('no connections right now')


if __name__ == "__main__":
    address = ("localhost", 5555)
    server_socket = create_server(address)
    event_loop(server_socket)
