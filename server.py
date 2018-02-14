import time
import json
import snap
import db
import os

import numpy as np
from flask import *
app = Flask(__name__)

lenThreshold = 1
globalList = []
print("PID: ", os.getpid())

def Pushtodb(Snappedlist):
    print("pushing to DB...")
    for row in Snappedlist:
        db.db_insert(row[0],row[1],row[2],row[3])

@app.route("/")
def index():
    return "Index!"
@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/events', methods=['POST'])
def events():
    global globalList
    global lenThreshold
    dummyList = [request.form.get('id'),request.form.get('lat'),request.form.get('lng'), request.form.get('time')]
    globalList.append(dummyList)

    if (len(globalList) > lenThreshold):
        print("Original list: \n", globalList, "\n")
        prevOldest = [request.form.get('id'),"37.67030362", "-122.46611581","1518010856"]
        globalList.insert(0, prevOldest)
        print("NEW list: \n", globalList)
        snappedlist = snap.snap_to_road(globalList, True)
        globalList = []

        #Delete overlaying points on same trip
        delete_list = []
        for i, row in enumerate(snappedlist[:-1]):
            if np.all(row == snappedlist[i + 1]):
                delete_list.append(i)
        snappedlist = np.delete(snappedlist, delete_list, axis=0)

        Pushtodb(snappedlist)

    return "ok"


@app.route('/api', methods=['GET', 'POST'])
def api():
    data = db.db_getpoints()
    return data

@app.route('/login', methods=['POST'])
def login():
    print(request.form.get)
    type_ = request.form.get('type')
    idn = db.db_newtrip(type_)
    print('login id:', idn)
    return idn


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
