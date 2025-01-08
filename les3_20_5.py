import asyncio

semaphore = asyncio.Semaphore(2)


async def semaphored_coro():
    if not semaphore.locked():
        async with semaphore:
            await get_data()
            await get_request()
    else:
        await get_another_job()
