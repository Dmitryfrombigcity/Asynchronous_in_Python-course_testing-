# server
import asyncio
import functools
import random
from time import time
from typing import Self


class Singleton(asyncio.Future):
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


async def helper(
        fut: Singleton,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:
    if not fut.done():
        fut.set_result(True)
    await handler(reader, writer)


async def _timer(fut: Singleton) -> None:
    while True:
        try:
            await asyncio.wait_for(asyncio.shield(fut), timeout=2)
        except TimeoutError:
            print(f">> {time():.3f} <<-- no connections right now")
        fut = Singleton()


async def handler(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:
    data = await reader.read(1024)
    data_str = data.decode()
    client, *data_lst = data_str.split()
    port = writer.transport.get_extra_info('peername')[-1]
    print(f">> {time():.3f} <<--from {client}:{port} received data << {data!r}")
    try:
        numbers = [int(n) for n in data_lst]
        res = sum(numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        await asyncio.sleep(random.randint(0, 5))
        writer.write(msg.encode())
        await writer.drain()
        print(f">> {time():.3f} --->>to  {client}:{port} sent answer   >> {msg!r}")
        writer.close()
        await writer.wait_closed()


async def main(
        address: tuple[str, int]
) -> None:
    fut = Singleton()
    _helper = functools.partial(helper, fut)
    server = await asyncio.start_server(_helper, *address)
    await _timer(fut)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    address = ("localhost", 5555)
    asyncio.run(main(address))
