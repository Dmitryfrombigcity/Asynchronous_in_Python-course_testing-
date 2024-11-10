import selectors
import socket


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, selectors.EVENT_READ, accept_conn)
        while True:
            if not (sentinel := sel.select(timeout=2)):
                print('Нет новых запросов за отведенный таймаут. Завершаем event_loop.')
                break
            for k, _ in sentinel:
                sock: socket.socket = k.fileobj
                callback = k.data
                try:
                    callback(sock, sel)
                except socket.error as e:
                    print("Потеря связи с клиентом. Закрываем сокет, снимаем с регистрации.")
                    sock.close()
                    sel.unregister(sock)
