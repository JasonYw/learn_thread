import asyncio
import asyncio
from asyncio import tasks
import time
import aiohttp

def test(number):
    start =time.time()

    async def get(url):
        session = aiohttp.ClientSession()
        response =await session.get(url)
        await response.text()
        await session.close()
        return response

    async def request():
        url ='https://www.baidu.com'
        await get(url)

    tasks =[asyncio.ensure_future(request()) for _ in range(number)]
    loop =asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end =time.time()
    print(end-start)

for number in [1,3,5,10,15,100,200,300,400,500]:
    test(number) 