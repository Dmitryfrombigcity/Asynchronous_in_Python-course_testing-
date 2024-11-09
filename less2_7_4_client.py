# client
import random
import socket
from multiprocessing import Process, current_process
from string import ascii_letters
from time import perf_counter, sleep


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    while True:
        messages = [int(temp)
                    if (temp := round(random.random(), random.randint(0, 3)) * random.choice((10, 100, 1000)))
                    else random.choice(ascii_letters)
                    for _ in range(random.randint(1, 5))
                    ]
        msg = ' '.join(map(str, messages))
        start = perf_counter()
        client_sock.send(msg.encode())
        response = client_sock.recv(1024)
        print(
            f'{current_process().name}>> '
            f'Response from server: {response.decode():60} '
            f'time response = {perf_counter() - start:.2f}s'
        )
        sleep(random.randint(0, 20))
    client_sock.close()


if __name__ == "__main__":
    for ind in range(5):
        Process(target=client, name=f'Process_{ind}').start()
