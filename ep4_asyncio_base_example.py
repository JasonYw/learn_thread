import asyncio
from asyncio.tasks import sleep

async def hello(i):
    print('hello',i)
    await asyncio.sleep(3)
    print('word',i)

if __name__ =="__main__":
    tasks =[]
    for  i in range(4):
        tasks.append(hello(i))
    loop =asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

