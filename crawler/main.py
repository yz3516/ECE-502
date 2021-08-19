#<<<<<<< HEAD
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sqlite3
from databaseManage import * 
from tkinter import *
import tkinter as tk

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
    root.title('Url-Crawler')
	#窗口的大小，后面的加号是窗口在整个屏幕的位置
    root.geometry('800x600')
	#标签控件，窗口中放置文本组件
    Label(root,text='Input the Website Address :',font=("arial",16),fg='black').grid(sticky = W, 
    columnspan = 2, ipadx = 5, ipady = 5)

	#Entry是可输入文本框
    global url_input
    url_input=Entry(root,font=("arial",16), width= 40)
    url_input.grid(sticky = W, row=1, column=0, columnspan = 2, ipadx = 5, ipady = 5)

    # add text box here
    outputBox = Text(root, font=("arial",16), height = 20, width=60)
    outputBox.grid(sticky = W, row = 2, column = 0, columnspan = 2, ipadx = 5, ipady = 5)
    #quote = """HAMLET: To be, """
    #outputBox.insert(END, quote)

    #设置按钮
    button_D = Button(root, text='Crawl!', font=("arial",16),command = lambda: crawl(outputBox))
    button_D.grid(sticky = W, row=3,column=0)
    button_E = Button(root, text='Exit',font = ("arial", 16),command = root.quit)
    button_E.grid(sticky = W, row=3,column=1)

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
def create_jobs(outputBox):
    for link in file_to_set(QUEUE_FILE):
        #if current link has not being crawled then append it to queue
        if not findChecked(cur, link): 
            queue.put(link)
    queue.join()
    crawl(outputBox)

# Check if there are items in the queue, if so crawl them
def crawl(outputBox):
    outputBox.delete('1.0', END)
    outputBox.insert(END, '''Crawling start, please wait.  \n''')
    HOMEPAGE = url_input.get()
    #HOMEPAGE = 'http://itu.edu/'
    DOMAIN_NAME = get_domain_name(url_input.get())
    Spider(PROJECT_NAME, url_input.get(), DOMAIN_NAME)

    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(outputBox)
    if (len(queued_links) == 0):
        processCrawled(cur, CRAWLED_FILE)
        result = printAll(cur)

        outputBox.insert(END, '''Crawling finished, these websites are crawled:  \n''')
        outputBox.insert(END, result)



def main():
    create_workers()
    callGUI()


    
    # printAll(cur)
    # close database connection 
    conn.close()

if __name__ == '__main__':
    main()

