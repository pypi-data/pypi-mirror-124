<p align="center">
    <a href="https://bit.ly/search-me-server"><img src="https://bit.ly/search-me-server-logo" width="500px" alt="SEARCH-ME-SERVER"></a>
</p>
<p align="center">
    <a href="https://bit.ly/search-me-server-paypal"><img src="https://bit.ly/search-me-server-logo-paypal" width="200px" alt="PayPal"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/search-me-server"><img src="https://img.shields.io/pypi/v/search-me-server.svg?style=flat-square&logo=appveyor" alt="Version"></a>
    <a href="https://pypi.org/project/search-me-server"><img src="https://img.shields.io/pypi/l/search-me-server.svg?style=flat-square&logo=appveyor" alt="License"></a>
    <a href="https://pypi.org/project/search-me-server"><img src="https://img.shields.io/pypi/pyversions/search-me-server.svg?style=flat-square&logo=appveyor" alt="Python"></a>
    <a href="https://pypi.org/project/search-me-server"><img src="https://img.shields.io/pypi/status/search-me-server.svg?style=flat-square&logo=appveyor" alt="Status"></a>
    <a href="https://pypi.org/project/search-me-server"><img src="https://img.shields.io/pypi/format/search-me-server.svg?style=flat-square&logo=appveyor" alt="Format"></a>
    <a href="https://pepy.tech/project/search-me-server"><img src="https://static.pepy.tech/personalized-badge/search-me-server?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads" alt="Downloads"></a>
    <br><br><br>
</p>

# ASYNC SEARCH-ME-SERVER

## PRE-INSTALLING

Look the page of [search-me](https://bit.ly/search--me)

## INSTALLING

```bash
pip install search-me-server
```

## SERVER

```python
import logging
from search_me import Google
from search_me_server import SearchMeServer


logging.basicConfig(level=logging.DEBUG)


server = SearchMeServer(
    log=True,
    log_options={
        'file': 'main.log',
        'size': 100000000,
        'format': '%(asctime)s	|	%(levelname)s	|	%(message)s',
        'buffer': 16384
        },
    server={
        'host': '127.0.0.1',
        'port': 8080,
        'api': '/',
        'log_format': '%t	|	%s	|	%a	|	%Tf'
        },
    engine=Google(
        **{
            "app": {
                "interactive": False
                },
            "web": {},
            "pdf": {},
            "social": {}
        }
    )
    )
# Logs enable on http://127.0.0.1:8080/logs
# server = SearchMeServer()
server.run()

```

## CLIENT

```python
import asyncio
import aiohttp


async def main(server, q):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{server}?q={q}") as resp:
            async for data, chunk in resp.content.iter_chunks():
                if chunk:
                    print(data)


SERVER_URL = "http://127.0.0.1:8080/"
Q = "0X0007EE"

loop = asyncio.get_event_loop()
loop.run_until_complete(main(
    server=SERVER_URL,
    q=Q
    ))

```
