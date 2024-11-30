# server
import asyncio
import contextvars
import random
from time import time, perf_counter


async def _timer() -> None:
    delta = 0.
    interval = 2
    while True:
        await asyncio.sleep(interval - delta)
        timer_time = perf_counter()
        delta = timer_time - sentinel.get()
        if delta > interval:
            print(f">> {time():.3f} <<-- no connections right now")
            sentinel.set(timer_time)


async def handler(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
) -> None:
    ctx.run(sentinel.set, perf_counter())
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
    server = await asyncio.start_server(handler, *address)
    async with server:
        timer = asyncio.create_task(_timer(), context=ctx)
        await server.serve_forever()


if __name__ == "__main__":
    sentinel: contextvars.ContextVar[float] = contextvars.ContextVar('sentinel')
    sentinel.set(perf_counter())
    ctx = contextvars.copy_context()
    address = ("localhost", 5555)
    asyncio.run(main(address))
