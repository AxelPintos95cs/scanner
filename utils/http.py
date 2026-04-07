import aiohttp
import asyncio

session = None

async def get_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()
    return session

async def get(url):
    try:
        session = await get_session()

        async with session.get(url, timeout=10) as response:
            text = await response.text()
            return response, text

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return None, None

async def close():
    global session
    if session:
        await session.close()
        session = None