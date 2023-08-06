# tpdne-py
### a very simple wrapper around requests/aiohttp for thispersondoesnotexist.com
#### provides 2 objects, Person and Aioperson. usage:
```
from tpdne import Person

def main() -> None:
    x = Person()
    with open('test.png', 'wb') as f:
        f.write(x.bytes)

if __name__ == "__main__":
    main()
```

```
from tpdne import AioPerson
import asyncio

async def main() -> None:
    x = await AioPerson()
    with open('test.png', 'wb') as f:
        f.write(x.bytes)

if __name__ == "__main__":
    asyncio.run(main())
```
#### optionally `fetch=False` can be passed to either constructor so that the image can be fetched at a later time with `Person.fetch()` or `await AioPerson.fetch()`

```
from tpdne import Person

def main() -> None:
    x = Person(fetch=False)
    # do something
    bytes = x.fetch()
    with open('test.png', 'wb') as f:
        f.write(bytes)

if __name__ == "__main__":
    main()
```

```
from tpdne import AioPerson
import asyncio

async def main() -> None:
    x = await AioPerson(fetch=False)
    # do something
    bytes = await x.fetch()
    with open('test.png', 'wb') as f:
        f.write(bytes)

if __name__ == "__main__":
    asyncio.run(main())
```
#### fetch returns `bytes` so there is no need to directly access `.bytes` when manually fetching (fetch also updates the instance attribute on first invocation)
