import asyncio
from time import perf_counter
from urllib.parse import urlparse

sources = ["https://yandex.ru:80",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru",
           "https://яndex.ru",
           "https://www.youtube.com",
           "https://www.porshe.de",
           "https://www.whatsapp.com",
           "https://www.baidu.com"
           ]


async def get_headers(url: str) -> None:
    start = perf_counter()
    hostname = urlparse(url).hostname
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(hostname, 443, ssl=True), timeout=15
        )
        query = (
            f"HEAD / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
        )

        writer.write(query.encode())
        await writer.drain()
        line = await reader.readline()
        status = line.decode().rstrip().lstrip('HTTP/1.1 ')
        writer.close()
        await writer.wait_closed()
        print(
            f"site:{hostname:30}--> status:{status:20} --> response {perf_counter() - start:.2f}c."
        )
    except Exception as err:
        print(
            f"site:{hostname:30}--> error :{err.__class__.__name__:20}"
        )


async def main() -> None:
    tasks = [get_headers(source) for source in sources]
    print("Connection is limited by a timeout of 15 seconds")
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
