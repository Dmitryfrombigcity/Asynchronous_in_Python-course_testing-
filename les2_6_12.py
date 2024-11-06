import socket
import threading
from threading import Thread, current_thread
from types import EllipsisType

lock = threading.Lock()


def handler(conn: socket.socket) -> None:
    while data := conn.recv(1024):
        print(f'{current_thread().name}>> received data {data!r}\n', end='')
        try:
            numbers = [int(n) for n in data.decode().split()]
            res = sum(numbers)
        except Exception as er:
            msg = repr(er)
        else:
            msg = f'{"+".join(map(str, numbers))}={res}'
        finally:
            conn.send(msg.encode())
    print(f'{current_thread().name}>> closed\n', end='')


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen(2)
    while True:
        print('Waiting for connections...\n', end='')
        conn, addr = server_sock.accept()
        print(f'server>> Connection from {addr}\n', end='')
        Thread(
            target=handler,
            args=(conn,),
            name=f'socket:{addr[-1]}'
        ).start()


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    msg: str | EllipsisType = ...
    while msg:
        with lock:
            msg = input(f"{current_thread().name}>> Enter the numbers to calculate: \n")
            match msg:
                case 'kill':
                    print(f'{current_thread().name}>> closed\n', end='')
                    client_sock.close()
                    break
                case '':
                    print(f'{current_thread().name}>> nothing sent\n', end='')
                    msg = ...
                    continue
                case _:
                    client_sock.send(msg.encode())
        response = client_sock.recv(1024)
        print(f'{current_thread().name}>> Response from server: {response.decode()}\n', end='')


def main() -> None:
    thrs: list[Thread] = []
    for name in ('first_client', 'second_client'):
        thr = Thread(target=client, name=name)
        thrs.append(thr)
        thrs[-1].start()

    server()


if __name__ == "__main__":
    main()
