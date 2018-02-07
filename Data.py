
import _thread
import time
import requests

print("kjorer 3 threads som alle sender HTTP post")

def SpamPrint(id):
    while(1):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://httpbin.org/post", data=payload)
        print(r.text)
        time.sleep(5)

_thread.start_new_thread ( SpamPrint, (1, ))
_thread.start_new_thread ( SpamPrint, (2, ))

while 1:
   pass