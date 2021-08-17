import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sqlite3
from databaseManage import * 
from tkinter import *

PROJECT_NAME = 'ITU'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

conn = sqlite3.connect('crawledList.db')
cur = conn.cursor()
# setup the url table if not already exist
add_url_table(cur)

def callGUI():
	# global url_input,text
	#创建空白窗口,作为主载体
    
    root = Tk()
    root.title('test')
	#窗口的大小，后面的加号是窗口在整个屏幕的位置
    root.geometry('550x400+398+279')
	#标签控件，窗口中放置文本组件
    Label(root,text='Input the Website Address :',font=("arial",20),fg='black').grid()
	#定位 pack包 place位置 grid是网格式的布局
	
	#Entry是可输入文本框
    url_input=Entry(root,font=("arial",15))
    url_input.grid(row=0,column=1)
	#列表控件
    text=Listbox(root,font=('arial',15),width=45,height=10)
	#columnspan 组件所跨越的列数
    text.grid(row=1,columnspan=2)
	
    #设置按钮 sticky对齐方式，N S W E
    button_D = Button(root, text='Download', font=("arial",15),command = lambda: crawl(url_input))
    button_D.grid(row=2,column=0,sticky=W)
    button_E = Button(root, text='Exit',font = ("arial", 15),command = root.quit)
    button_E.grid(row=2,column=1,sticky=E)
	
    #使得窗口一直存在
    mainloop()

# Create worker threads (will die when main exits)
def create_workers(queue):
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work(queue))
        t.daemon = True
        t.start()


# Do the next job in the queue
def work(queue):
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(queue):
    for link in file_to_set(QUEUE_FILE):
        #if current link has not being crawled then append it to queue
        if not findChecked(cur, link): 
            queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl(url_input):
    
    #HOMEPAGE = url_input.get()
    HOMEPAGE = 'itu.com'
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    queue = Queue()
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
    create_workers(queue)

    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(queue)


def main():
    
    callGUI()

    processCrawled(cur)
    printAll(cur)
    # close database connection 
    conn.close()

if __name__ == '__main__':
    main()
