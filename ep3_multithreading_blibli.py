#coding:utf-8
from queue import Queue
import threading
import json
import requests
import time

session =requests.session()
class Threadcrawl(threading.Thread):
    def __init__(self,threadname,pageque,dataque):
        super(Threadcrawl,self).__init__()
        self.threadname =threadname
        self.pageque =pageque
        self.dataque =dataque
        self.headers ={
            'authority': 'api.bilibili.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            #'cookie': #input your cookie
            'referer': 'https://space.bilibili.com/284453579/fans/fans',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }
       
    def run(self):
        print(self.threadname,'start')
        try:
            pn =self.pageque.get(False)
            url ="https://api.bilibili.com/x/relation/followers?vmid=284453579&pn=" + str(pn) + "&ps=20&order=desc&jsonp=jsonp"
            self.headers['path'] = "/x/relation/followers?vmid=284453579&pn=" +str(pn)+ "&ps=20&order=desc&jsonp=jsonp"
            print(url)
            time.sleep(1)
            response =session.get(url=url,headers=self.headers,timeout=2)
            self.dataque.put(response)
        except Exception as e:
            print(e)
        print(self.threadname,'done')

class Threadparse(threading.Thread):
    def __init__(self,threadname,dataque,filename,lock):
        super(Threadparse,self).__init__()
        self.threadname =threadname
        self.dataque =dataque
        self.filename =filename
        self.lock =lock

    def run(self):
        print(self.threadname,'start')
        try:
            js_data =self.dataque.get(False)
            content =json.loads(js_data.text)
            self.parse_jsdata(content)
        except Exception as e:
            print(e)
        print(self.threadname,'done')
    
    def parse_jsdata(self,content):
        for i in content['data']['list']:
            item ={}
            item['id'] =i['mid']
            item['name'] =i['uname']
            self.write_jsdata(item)

    def write_jsdata(self,item):
        print('writing',item)
        try:
            need_to_write =json.dumps(item,ensure_ascii=False).encode("utf-8")+'\n'
        except:
            need_to_write =json.dumps(item,ensure_ascii=False)+'\n'
        with self.lock:
            self.filename.write(need_to_write)




def main():
    threading_crawllist =["爬取队列1","爬取队列2","爬取队列3","爬取队列4","爬取队列5"]
    threading_parselist =["处理队列1","处理队列2","处理队列3","处理队列4","处理队列5"]
    pageque =Queue()
    dataque =Queue()
    lock =threading.Lock()
    filename =open("blibli_followers_name_id.json",'a')

    #更改range()函数第二个参数，可决定爬取的页数
    for i in range(1,101):
        pageque.put(i)

    crawlthreadinglist =[]
    parsethreadinglist =[]
    
    #爬取队列
    while not pageque.empty():
        for threadname in threading_crawllist:
            thread =Threadcrawl(threadname,pageque,dataque)
            thread.start()
            crawlthreadinglist.append(thread)
    
        
    for threadname in crawlthreadinglist:
        threadname.join()

    #采集队列
    while not dataque.empty():
        for threadname in threading_parselist:
            thread =Threadparse(threadname,dataque,filename,lock)
            thread.start() 
            parsethreadinglist.append(thread)
    
    for threadname in parsethreadinglist:
        threadname.join()
    
    with lock:
        filename.close()

if __name__ == "__main__":
    main()