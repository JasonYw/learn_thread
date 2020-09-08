import asyncio
import aiohttp
import time

starttime =time.time()
async def get(url):
    session = aiohttp.ClientSession()
    response =await session.get(url)
    print('session.get()',url)
    await response.text()
    print('response.text()',url)
    await session.close()
    print('session.close()',url)
    return response

async def request(page):
    url ='https://static4.scrape.cuiqingcai.com/page/'+str(page)
    print('waiting for',url)
    response =await get(url)
    print('GET response for',url,'response',response.status)

tasks =[asyncio.ensure_future(request(_)) for _ in range(1,11)]
loop =asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
endtime =time.time()
print('cost:',endtime-starttime)