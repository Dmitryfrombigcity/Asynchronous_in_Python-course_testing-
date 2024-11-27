# server
import asyncio
import random


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = await reader.read(1024)
    data_str = data.decode()
    client, *data_lst = data_str.split()
    port = writer.transport.get_extra_info('peername')[-1]
    print(f"<<--from {client}:{port} received data << {data!r}")
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
        print(f"--->>to  {client}:{port} sent answer   >> {msg!r}")
        writer.close()
        await writer.wait_closed()


async def main(address: tuple[str, int]) -> None:
    server = await asyncio.start_server(handler,  *address)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    address = ("localhost", 5555)
    asyncio.run(main(address))
