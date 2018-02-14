import time
import json
import snap
import db
import os
from flask_cors import CORS

import numpy as np
from flask import *
app = Flask(__name__)
CORS(app)

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
    positionlist = []
    print("New set of positions from client!")
    print("getlist: \n", request.form.getlist('lat'))

    fromDB = (db.db_getnewest(request.form.get('id')))

    # HER SKAL DU SETTE INN TIL "VANLIG" LISTE STRUKTUR MARKUS

    if (fromDB is not None):
        temp = json.loads(fromDB)
        prevOldest = [temp['id'], temp['lat'], temp['lng'], temp['time']]
        positionlist.insert(0, prevOldest)
    snappedlist = snap.snap_to_road(positionlist, True)

    #Delete overlaying points on same trip
    delete_list = []
    for i, row in enumerate(snappedlist[:-1]):
        if np.all(row == snappedlist[i + 1]):
            delete_list.append(i)
    snappedlist = np.delete(snappedlist, delete_list, axis=0)

   # Pushtodb(snappedlist)
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
    print('login id:', idn, " with type_: ", type, " and type_", type_)
    return str(idn)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
