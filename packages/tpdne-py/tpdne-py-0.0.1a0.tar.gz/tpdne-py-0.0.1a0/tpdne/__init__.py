import requests
import aiohttp

url = "https://thispersondoesnotexist.com/image"

class async_init(object):
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass

class AioPerson(async_init):
    __slots__ = ('bytes')

    async def __init__(self, *, fetch: bool=True) -> object:
        if fetch:
            await self.fetch()

    async def fetch(self) -> bytes:
        if not hasattr(self, 'bytes'):
            async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        self.bytes = await resp.read()
        return self.bytes

class Person():
    __slots__ = ('bytes')

    def __init__(self, fetch: bool=True) -> object:
        if fetch:
            self.fetch()

    def fetch(self) -> bytes:
        if not hasattr(self, 'bytes'):
            self.bytes = requests.get(url).content
        else:
            print('already fetched but ok')
        return self.bytes