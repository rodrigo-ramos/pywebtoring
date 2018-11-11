# 
# 
# Hace un monitoreo de URL's con hilos.
# Se invoca la URL y registra el código de respuesta HTTP, el tiempo 
# transcurrido y si hubo alguna excepción.
# 

import requests
import time
import threading
from queue import Queue
import sqlite3
import datetime

print ("PyWebToring is working...")

# Definicion de la BD
sqlfile = '../db/pywebtoring_store.db'
table_name ='urls'
colname_timestamp = 'date'
colname_url = 'url'
colname_response_time = 'response_time'
colname_httpcode = 'response_code'
colname_exception = 'ex_http'

urls = [one_line.strip()
        for one_line in open('../url_files/pywebtoring_urls.txt')]
length = {}
queue = Queue()
start_time = time.time()
threads = []

def get_length(one_url):
        response_code=0
        response_time=0
        response=""
        ex_http = "NA"

        try:
                response = requests.get(one_url)
                response_code = response.status_code
                response_time = response.elapsed.total_seconds()

        except Exception as ex:
                #print (ex)
                ex_http = ex
        finally:
                queue.put((str(datetime.datetime.now()),one_url,response_time,response_code,str(ex_http)))


for one_url in urls:
        t = threading.Thread(target=get_length, args=(one_url,))
        threads.append(t)
        t.start()
print ("Joining")
for one_thread in threads:
        one_thread.join()
print ("Retrieve and printing")
conn = sqlite3.connect(sqlfile)
while not queue.empty():
        #one_url, response_time, response_code, ex_http = queue.get()
        rows = queue.get()
        print (rows)
        conn.execute('insert into urls values (?,?,?,?,?)',rows)
        #print ("{0} {1:30} {2} {3} {4}".format(datetime.datetime.now(),one_url,response_time,response_code,ex_http))

conn.commit()
conn.close()

end_time = time.time()
total_time = end_time - start_time
print("Total time : {0:3} seconds ".format(total_time))
