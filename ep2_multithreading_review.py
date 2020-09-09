#coding:utf-8
#使用了线程库
import threading
from queue import Queue
from lxml import etree
import requests
import json

class ThreadCrawl(threading.Thread):

    def __init__(self,threadname,pageQue,dataQue):
        #继承
        #threading.Thread.__init__(self) 
        #调用父类初始化
        super(ThreadCrawl,self).__init__()
        #线程名
        self.threadname =threadname
        #页码队列
        self.pageQue =pageQue
        #数据队列
        self.dataQue =dataQue
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }

    
    def run(self):
        print("启动"+self.threadname)
    
        # while not self.pageQue.empty():
        try:
            #取出一个数字
            #可选参数block，默认值为true
            #如果队列为空，block为ture的话，不会结束，就会进入阻塞状态，等直到 队列有新的数据
            #如果队列为空，block为false的话，就会弹出一个队列为空的异常
            page =self.pageQue.get(False)
            if int(page) ==1:
                url ='http://www.yicommunity.com/zuixin/index.html'
            else:
                url ='http://www.yicommunity.com/zuixin/index_'+str(page)+'.html'
            print('linking:',url)
            content =requests.get(url=url,headers=self.headers)
            self.dataQue.put(content)
        except:
            pass

        print("结束"+self.threadname)
  
  


class ThreadParse(threading.Thread):

    def __init__(self,threadname,dataQue):
        super(ThreadParse,self).__init__()
        self.threadname =threadname
        self.dataQue =dataQue

    def run(self):
        print("启动",self.threadname)
        #pageQue.empty()为空时，返回True
        try:
            html =self.dataQue.get(False)
            self.parse(html)
        except:
            pass
        print("结束"+self.threadname)


    def parse(self,html):
        html_jiexi =etree.HTML(html)
        node_list =html_jiexi.xpath('//div[@class="block untagged mb15 bs2"]')
        items={}
        for node in node_list:
            print('xpathing')
            username =node.xpath('.//@alt')[0]

            #取出正文
            usertext =node.xpath('.//div[@class="content"]')[0].text.strip()

            #取出点赞数
            userupp =node.xpath('.//li[@class="up"]')[0].text

            #取出评论
            usercomment =node.xpath('.//li[@class="comment"]')[0].text

            items ={
                'writer: ': username,
                'body: ': usertext,
                'like: ': userupp,
                'comment: ': usercomment
            }
            print('wirting',items) 


def main():
    #页码的队列，表示10个页面
    pageQue =Queue(10)
    #先进先出，放入1-10
    for i in range(1,11):
        pageQue.put(i)

    #采集结果的数据队列，参数为空表示不限制
    dataQue =Queue()

    #采集线程名字
    crwalList =['采集线程1号','采集线程2号','采集线程3号']

    #解析线程
    parselist =["解析线程1号","解析线程2号","解析线程3号"]

    #存储三个采集线程的名字
    threadcrawl =[]
    #存储三个解析线程的名字
    threadparse=[]

    while not pageQue.empty():
        for threadname in crwalList:
            #print(threadname)
            thread =ThreadCrawl(threadname,pageQue,dataQue)
            thread.start()
            thread.join()
            threadcrawl.append(thread)

    while not dataQue.empty():
        for threadname in parselist:
            #print(threadname)
            thread =ThreadParse(threadname,dataQue)
            thread.start()
            thread.join()
            threadparse.append(threadname)
    
    for thread in threadcrawl:
        thread.join()
        
    for thread in threadcrawl:
        thread.join()
  


if __name__ =="__main__":
    main()


