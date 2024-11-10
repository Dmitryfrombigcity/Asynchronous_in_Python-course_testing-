import selectors
import socket
from typing import Any


def accept_conn(server_sock: socket.socket, sel: selectors.BaseSelector) -> None:
    try:
        conn, addr = server_sock.accept()
        sel.register(conn, selectors.EVENT_READ, send_response)
    except socket.error as e:
        print(f"Error accepting connection: {e}")


def send_response(client_sock: socket.socket, *args: Any) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, selectors.EVENT_READ, accept_conn)
        while True:
            for k, _ in sel.select():
                sock: socket.socket = k.fileobj
                callback = k.data
                try:
                    callback(sock, sel)
                except socket.error as e:
                    print("Потеря связи с клиентом. Закрываем сокет, снимаем с регистрации.")
                    sock.close()
                    sel.unregister(sock)
