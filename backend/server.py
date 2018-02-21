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
    # positionlist = []
    print("New set of positions from client!")
    print("getlist: \n", request.form.getlist('lat'))


    idn = np.array(request.form.getlist('id'))
    lat = np.array(request.form.getlist('lat'))
    lng = np.array(request.form.getlist('lng'))
    time = np.array(request.form.getlist('time'))
    data = np.array([idn, lat, lng, time])
    data = np.transpose(data)


    fromDB = (db.db_getnewest(request.form.get('id')))
    if (fromDB is not None):
        temp = json.loads(fromDB)
        prevOldest = np.array([[temp['id'], temp['lat'], temp['lng'], temp['time']]])
        # positionlist.insert(0, prevOldest)
        data = np.concatenate([prevOldest, data], axis=0)

    print('data:', data.shape)
    print(data)

    snappedlist = snap.snap_to_road(data, interpolate=False)

    #Delete overlaying points on same trip
    delete_list = []
    for i, row in enumerate(snappedlist[:-1]):
        if np.all(row == snappedlist[i + 1]):
            delete_list.append(i)
    snappedlist = np.delete(snappedlist, delete_list, axis=0)


    ##  DATALOGGER
    text_file = open("Output.txt", "a")
    for i in range(len(snappedlist)):
        #print("NEWSTER: \n", lat, "\n", lat[0])
        text_file.write("id: '{0}', lat lng {1}, {2} \n".format( snappedlist[i][0], snappedlist[i][1], snappedlist[i][2] ))
    text_file.close()
    print("SNAP:", snappedlist)
    ##

    ##  DATALOGGER 2
    text_file2 = open("Output2.txt", "a")
    text_file2.write("\n \n Setter ny inn i DB\n")
    text_file2.write("%s" % snappedlist)
    text_file2.close()
    ##

    Pushtodb(snappedlist)
    return "ok"


@app.route('/api', methods=['GET', 'POST'])
def api():
    data = db.db_getpoints()
    print("return data: ", data)
    return data

@app.route('/login', methods=['POST'])
def login():
    print(request.form.get)
    type_ = request.form.get('type')
    idn = db.db_newtrip(type_)
    print('login id:',idn, " and type_", type_)
    return str(idn)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
