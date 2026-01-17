import asyncio
import ssl

import aiohttp
import certifi

_ssl_context = ssl.create_default_context(cafile=certifi.where())


def new_client_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=_ssl_context))


async def main():
    url = "https://www.python.org"

    async with new_client_session() as session:
        print(f"正在请求: {url}")

        async with session.get(url) as response:
            print(f"状态码: {response.status}")

            html = await response.text()
            print(f"页面长度: {len(html)} 字符")


if __name__ == "__main__":
    asyncio.run(main())
