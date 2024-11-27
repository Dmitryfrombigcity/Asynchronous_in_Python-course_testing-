# client
import asyncio
import random
from asyncio import TaskGroup
from string import ascii_letters
from time import perf_counter


async def helper(address: tuple[str, int]) -> None:
    while True:
        start = perf_counter()
        reader, writer = await asyncio.open_connection(*address)
        port = writer.transport.get_extra_info('sockname')[-1]
        messages = [asyncio.current_task().get_name()]  # type:ignore
        messages.extend(
            [int(temp)
             if (temp := round(random.random(), random.randint(0, 3)) * random.choice((10, 100, 1000)))
             else random.choice(ascii_letters)
             for _ in range(random.randint(1, 5))
             ]
        )
        msg = ' '.join(map(str, messages))
        writer.write(msg.encode())
        await writer.drain()
        data = await reader.read(1024)
        print(
            f'{asyncio.current_task().get_name()}:{port}>> '  # type:ignore
            f'Response from server: {data.decode():60} '
            f'time response = {perf_counter() - start:.2f}s'
        )
        await asyncio.sleep(random.randint(0, 1))
    writer.close()
    await writer.wait_closed()


async def client(address: tuple[str, int]) -> None:
    async with TaskGroup() as group:
        for ind in range(1, 6):
            group.create_task(helper(address), name=f'client_{ind}')


if __name__ == "__main__":
    address = ("localhost", 5555)
    asyncio.run(client(address))
