import socket


def server(address: tuple[str, int]) -> None:
    sock = socket.socket()
    sock.bind(address)
    sock.listen()
    conn, _ = sock.accept()
    data = conn.recv(4096)
    print(sum(
        map(int, data.decode().split()))
    )
    sock.close()
