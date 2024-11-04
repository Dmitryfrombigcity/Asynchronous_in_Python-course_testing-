import socket


def client(address: tuple[str, int], msg: str) -> None:
    sock = socket.socket()
    sock.connect(address)
    sock.send(msg.encode())
    sock.close()
