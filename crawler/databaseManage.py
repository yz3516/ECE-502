import sqlite3
import datetime

# Create a Link class
class Link:

    def __init__(self, url, status, time):
        self.url = url
        self.status = status
        self.time = time
        
    def set_url(self, url):
        self.url = url
    
    def set_status(self, status):
        self.status = status
    
    def set_time(self, time):
        self.time = time
    
    def get_url(self):
        return self.url
    
    def get_status(self):
        return self.status
    
    def get_time(self):
        return self.time
        

def processCrawled(cur):
    crawlFile = open(CRAWLED_FILE, 'r')
    Lines = crawlFile.readlines()

    for row in Lines:
        current_time = datetime.datetime.now()
        data = Link(row, 'crawled', current_time)
        cur.execute('''INSERT INTO urlTable(url, status, time) VALUES(?,?,?)''', (data.get_url(), data.get_status(), data.get_time()))

def findChecked(cur, urlAddress):
    # search database with urlAddress and has a status of crawled
    #cur.execute(''' SELECT * FROM urlTable WHERE url = urlAddress AND status = 'crawled' ''')
    cur.execute(" SELECT * FROM urlTable WHERE url = ? AND status = 'crawled' ", (urlAddress,))
    urlList = cur.fetchall()
    if (len(urlList) > 0):
        return True
    else:
        return False
    
def printAll(cur):
    cur.execute("SELECT * FROM urlTable")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Create the table
def add_url_table(cur):
    cur.execute("DROP TABLE IF EXISTS urlTable")
    cur.execute('''CREATE TABLE urlTable(url TEXT, status TEXT, time TEXT)''')
                                   
