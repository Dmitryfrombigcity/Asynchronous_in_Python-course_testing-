import asyncio
import functools
from asyncio import CancelledError

#
# async def worker(data: str) -> str:
#     return 'Final'


async def _checker(
        server: asyncio.Server,
        sentinel: list[None]
) -> None:
    while True:
        await asyncio.sleep(2)
        print('--------------------->', len(sentinel))
        if not sentinel:
            server.close()
            await server.wait_closed()


async def handler(
        sentinel: list[None],
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,

) -> None:
    sentinel.append(None)
    data = await reader.read(1024)
    res = await worker(data.decode())
    writer.write(res.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    sentinel.pop()


async def main(address: tuple[str, int]) -> None:
    sentinel: list[None] = []
    _handler = functools.partial(handler, sentinel)
    server = await asyncio.start_server(_handler, *address)
    async with server:
        task = asyncio.create_task(_checker(server, sentinel))
        try:
            await server.serve_forever()
        except CancelledError:
            print('Работа сервера завершена!')

#
# if __name__ == "__main__":
#     address = ("localhost", 5555)
#     asyncio.run(main(address))
