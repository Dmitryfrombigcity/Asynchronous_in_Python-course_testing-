import asyncio


async def producer(queue: asyncio.PriorityQueue):
    async for elem in json_gen():
        await queue.put((0, elem))
    await queue.put((1, ...))


async def consumer(queue: asyncio.PriorityQueue):
    while True:
        sentinel, elem = await queue.get()
        if sentinel:
            await queue.put((1, ...))
            break
        await registrator(elem)


async def producer_consumer(queue: asyncio.PriorityQueue):
    await asyncio.gather(producer(queue), consumer(queue), consumer(queue))
    queue.get_nowait()
    final()
