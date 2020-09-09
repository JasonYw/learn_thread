import asyncio
import aiohttp
import mysql.connector
import threading
from bs4 import BeautifulSoup
from queue import Queue
from lxml import etree


class Thread_Parseresponse(threading.Thread):
    def __init__(self,threadname,pagequeue,dataqueue):
        super(Thread_Parseresponse,self).__init__()
        self.threadname =threadname
        self.pagequeue =pagequeue
        self.dataqueue =dataqueue

    def run(self):
        print(self.threadname,'-starting')
        try:
            html =self.pagequeue.get(False)
            data =etree.HTML(html)
            node_list =data.xpath('//div[contains(@class,"el-card item m-t is-hover-shadow")]')
            print(len(node_list))
            for node in node_list:
                try:
                    title =node.xpath('.//h2/text()')[0]
                except:
                    title =''

                try:
                    score =node.xpath('.//p[contains(@class,"score")]/text()')[0]
                except:
                    score=''

                try:
                    date =node.xpath('.//div[contains(@class,"m-v-sm info")][2]/span/text()')[0]
                except:
                    data=''    
                item ={}
                item['name'] =title
                item['score'] =score.replace('\n',"").replace(' ',"")
                item['date'] =date
                print(item)
                self.dataqueue.put(item)
            

        except Exception as e:
            print(e)

class Thread_Write_toMysql(threading.Thread):
    def __init__(self,threadname,dataqueue):
        super(Thread_Write_toMysql,self).__init__()
        self.threadname =threadname
        self.dataqueue =dataqueue
       
    def run(self):
        print(self.threadname,'-starting')
        try:
            item =self.dataqueue.get(False)
            name =item['name']
            score =item['score']
            date =item['date']
            connector =mysql.connector.connect(user='root',password='0125',database='py_write')
            cursor =connector.cursor()
            print('INSERT INTO db_movie (name,score,date) VALUES ("%s",%s,"%s")'%(name,score,date))
            cursor.execute('INSERT INTO db_movie (name,score,date) VALUES ("%s",%s,"%s")'%(name,score,date))
            connector.commit()
        except Exception as e:
            print(e)
                
class Crwalurl():
    def __init__(self):
        self.headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        }
        self.pagequeue =Queue()

    async def prase_url(self,url):
        session =aiohttp.ClientSession(headers=self.headers)
        print('starting linking:',url)
        response =await session.get(url)
        data = await response.text()
        self.pagequeue.put(data)
        await session.close()
        print("close:",url)

    async def run(self,page):
        url ='https://static4.scrape.cuiqingcai.com/page/'+str(page)
        await self.prase_url(url)
        

    def Thread_start(self):
        dataqueue =Queue()
        Thread_Parseresponsename =['Thread_Parseresponse1','Thread_Parseresponse2','Thread_Parseresponse3','Thread_Parseresponse4','Thread_Parseresponse5',]
        Thread_Write_toMysqlname =['Thread_Write_toMysql1','Thread_Write_toMysql2','Thread_Write_toMysql3','Thread_Write_toMysql4','Thread_Write_toMysql5',]
        junk_Thread_Parseresponse =[]
        junk_Thread_Write_toMysql =[]
        # Lock =threading.Lock()

        while not self.pagequeue.empty():
            for thread_ in Thread_Parseresponsename:
                thread = Thread_Parseresponse(thread_,self.pagequeue,dataqueue)
                thread.start()
                junk_Thread_Parseresponse.append(thread)

        for thread_ in junk_Thread_Parseresponse:
            thread_.join()

        while not dataqueue.empty():
            for thread_ in Thread_Write_toMysqlname:
                thread =Thread_Write_toMysql(thread_,dataqueue)
                thread.start()
                junk_Thread_Write_toMysql.append(thread)

        for  thread_ in junk_Thread_Write_toMysql:
            thread_.join()

        
def main():
    test_example =Crwalurl()
    tasks =[asyncio.ensure_future(test_example.run(_)) for _ in range(1,11)]
    loop =asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    test_example.Thread_start()
    

if __name__ =="__main__":
    main()





        

