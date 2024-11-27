import asyncio
from functools import reduce


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = await reader.read(1024)
    data_str = data.decode()
    try:
        numbers = [int(n) for n in data_str.split()]
        res = reduce(lambda x, y: x * y, numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"*".join(map(str, numbers))}={res}'
    finally:
        writer.write(msg.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()


async def main(address: tuple[str, int]) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        await server.serve_forever()

#
# if __name__ == "__main__":
#     address = ("localhost", 5555)
#     asyncio.run(main(address))
