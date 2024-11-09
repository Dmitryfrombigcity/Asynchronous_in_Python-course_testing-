# server
import random
import select
import socket
from time import sleep


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


def accept_conn(server_sock: socket.socket, sockets: list[socket.socket]) -> None:
    try:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        sockets.append(conn)
    except socket.error as error:
        print(f"Error accepting connection: {error}")


def send_response(client_sock: socket.socket) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    sockets = [server_socket]
    while sockets:
        sockets_for_read, _, _ = select.select(sockets, [], [], 2)
        if sockets_for_read:
            for sock in sockets_for_read:
                if sock is server_socket:
                    accept_conn(sock, sockets)
                else:
                    try:
                        send_response(sock)
                    except socket.error as error:
                        print(f"Error receiving data: {error}")
                        sock.close()
                        sockets.remove(sock)
        else:
            print('no connections right now')


if __name__ == "__main__":
    address = ("localhost", 5555)
    server_socket = create_server(address)
    event_loop(server_socket)
