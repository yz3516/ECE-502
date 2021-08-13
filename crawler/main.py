import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sqlite3
from databaseManage import * 

#GUI可能主要在这里让用户输入
PROJECT_NAME = 'ITU'
HOMEPAGE = 'http://itu.edu/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


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
def create_jobs(cur):
    for link in file_to_set(QUEUE_FILE):
        #if current link has not being crawled then append it to queue
        if not findChecked(cur, link): 
            queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl(cur):
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(cur)


def main():
    # get connected with database and setup cursor 
    conn = sqlite3.connect('crawledList.db')
    cur = conn.cursor()
    # setup the url table if not already exist
    add_url_table(cur)

    create_workers()
    crawl(cur)

    processCrawled(cur)
    printAll(cur)
    # close database connection 
    conn.close()

if __name__ == '__main__':
    main()
