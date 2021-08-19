<<<<<<< HEAD
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
queue = Queue()

conn = sqlite3.connect('crawledList.db')
cur = conn.cursor()
# setup the url table if not already exist
add_url_table(cur)

def callGUI():
	#创建空白窗口,作为主载体
    root = Tk()
    root.title('test')
	#窗口的大小，后面的加号是窗口在整个屏幕的位置
    root.geometry('800x200+400+300')
	#标签控件，窗口中放置文本组件
    Label(root,text='Input the Website Address :',font=("arial",20),fg='black').grid()

	#Entry是可输入文本框
    global url_input
    url_input=Entry(root,font=("arial",15))
    url_input.grid(row=0,column=2)

    #设置按钮
    button_D = Button(root, text='Start Crawling', font=("arial",15),command = lambda: [create_workers(),crawl()])
    button_D.grid(row=2,column=0)
    button_E = Button(root, text='Save the result in DB',font = ("arial", 15),command = lambda: db())
    button_E.grid(row=2,column=1)
    button_F = Button(root, text='Exit',font = ("arial", 15),command = root.quit)
    button_F.grid(row=2,column=2)

    #使得窗口一直存在
    mainloop()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        #if current link has not being crawled then append it to queue
        if not findChecked(cur, link):
            queue.put(link)
    queue.join()
    crawl()

# Check if there are items in the queue, if so crawl them
def crawl():
    HOMEPAGE = url_input.get()
    #HOMEPAGE = 'http://itu.edu/'
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def db():
    processCrawled(cur)
    printAll(cur)
    # close database connection
    conn.close()

def main():
    callGUI()

if __name__ == '__main__':
    main()
