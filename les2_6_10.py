import multiprocessing
import socket
import sys


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        while data := conn.recv(1024):
            print(f"received data {data!r}")
            try:
                numbers = [int(n) for n in data.decode().split()]
                res = sum(numbers)
            except Exception as er:
                msg = repr(er)
            else:
                msg = f'{"+".join(map(str, numbers))}={res}'
            finally:
                conn.send(msg.encode())


def client() -> None:
    sys.stdin = open(0)
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    while (msg := input("Enter the numbers to calculate: \n")) != "kill":
        client_sock.send(msg.encode())
        response = client_sock.recv(1024)
        print(f"Response from server: {response.decode()}")
    client_sock.close()


def main() -> None:
    multiprocessing.Process(target=server).start()
    multiprocessing.Process(target=client).start()


if __name__ == "__main__":
    main()
