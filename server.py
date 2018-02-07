import time
import json
import snap
import db
import os

import numpy as np
from flask import *
app = Flask(__name__)

globalList = []
print(os.getpid())
#db.db_newtrip('broyt','56')

def Pushtodb(Snappedlist):
    print("pushing to DB...")
   # for row in Snappedlist:
    #    db.db_insert(row[0],row[1],row[2],row[3])


@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/events', methods=['POST'])
def events():
#    os.getpid()
    print(request.form.get)
    print("\n \n New POST request... \n")
    dummyList = [request.form.get('id'),request.form.get('lat'),request.form.get('lng'), request.form.get('time')]
    print("dummy:", dummyList)
    global globalList
    globalList.append(dummyList)
    if (len(globalList) > 1):
        print("multiple entries:")
        print(globalList)
        snappedlist = snap.snap_to_road(globalList, True)
        print("new:")
        print(snappedlist.shape)
        globalList = []

        delete_list = []
        for i, row in enumerate(snappedlist[:-1]):
            if np.all(row == snappedlist[i + 1]):
                delete_list.append(i)
        snappedlist = np.delete(snappedlist, delete_list, axis=0)
        print(snappedlist.shape)
        print(snappedlist)

        Pushtodb(snappedlist)
    return "ok"


@app.route('/api', methods=['GET', 'POST'])
@crossdomain(origin='*')
def api():

    data = db.db_getpoints()
    print("DATA: ")
    print(data)
    #jasonify()
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
