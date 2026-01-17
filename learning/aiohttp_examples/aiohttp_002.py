import asyncio
import ssl
import time

import aiohttp
import certifi

_ssl_context = ssl.create_default_context(cafile=certifi.where())


def new_client_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=_ssl_context))


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return f"URL: {url}, 状态: {response.status}"
    except Exception as e:
        return f"URL: {url}, 出错: {e}"


async def main():
    urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.baidu.com",
        "https://www.stackoverflow.com",
    ]

    async with new_client_session() as session:
        tasks = []
        for url in urls:
            task = fetch_url(session, url)
            tasks.append(task)

        print("开始并发请求...")
        start_time = time.time()

        results = await asyncio.gather(*tasks)

        print(f"全部完成，耗时: {time.time() - start_time:.2f}秒")

        for res in results:
            print(res)


if __name__ == "__main__":
    asyncio.run(main())
