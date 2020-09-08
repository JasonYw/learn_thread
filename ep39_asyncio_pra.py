import asyncio
from wsgiref import headers
import aiohttp
import mysql.connector
import threading
from bs4 import BeautifulSoup
from queue import Queue


# class Thread_Parseresponse(threading.Thread):
#     def __init__(self,dataqueue):
#         super(Spy_cuiqingcai,self).__init__()

#     async def run(self,dataqueue):
#         while not dataqueue.empty():
#             try:
#                 html =dataqueue.get(False)
#                 soup =BeautifulSoup.soup(html,'lxml')
#                 title_list =soup.findall('h2',class_='m-b-sm')
#                 score_list =soup.findall('p',class_='score m-t-md m-b-n-sm')
#                 date_list =soup.findall('span',id='data-v-7f856186')
#                 for i in range(len(title_list)):
#                     item ={}
#                     item['name'] =title_list(i)
#                     item['score'] =score_list(i)
#                     item['date'] =date_list(i)
#                     await item
#             except:
#                 pass

class Crwalurl():
    def __init__(self):
        self.headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        }
        self.responselist =[]

    # @asyncio.coroutine
    # def save_response(self,response):
    #     yield from self.responselist.append(response.text)

    async def prase_url(self,url):
        session =aiohttp.ClientSession()
        print('starting linking:',url)
        response =await session.get(url)
        await session.close()


    async def run(self,page):
        url ='https://static4.scrape.cuiqingcai.com/page/'+str(page)
        self.prase_url(url)





def main():
    test_example =Crwalurl()
    print(test_example.run())


if __name__ =="__main__":
    main()





        

