import json
import snap
import db
import os
import NewDB
from flask_cors import CORS

import numpy as np
from flask import *
app = Flask(__name__)
CORS(app)
print("PID: ", os.getpid())

def Pushtodb(Snappedlist):
    for row in Snappedlist:
        NewDB.insertToDb(row[0],row[1],row[2],row[3])

@app.route("/")
@app.route("/<page>")
def index(page="index.html"):
    print(page)
    return Blueprint('cast', __name__, static_folder="../frontend/dist", static_url_path='').send_static_file(page)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/events', methods=['POST'])
def events():
    idn = np.array(request.form.getlist('id'))
    lat = np.array(request.form.getlist('lat'))
    lng = np.array(request.form.getlist('lng'))
    time = np.array(request.form.getlist('time'))
    data = np.array([idn, lat, lng, time])
    data = np.transpose(data)

    text_file2 = open("Output2.txt", "a")
    text_file2.write("\n \n Setter ny inn i DB\n")
    text_file2.write("raa data: \n%s" % data)

    fromDB = (db.db_getnewest(request.form.get('id')))
    if (fromDB is not None):
        temp = json.loads(fromDB)
        prevOldest = np.array([[temp['id'], temp['lat'], temp['lng'], temp['time']]])
        data = np.concatenate([prevOldest, data], axis=0)
    snappedlist = snap.snap_to_road(data, interpolate=True)

    #Delete overlaying points on same trip
    delete_list = []
    for i, row in enumerate(snappedlist[:-1]):
        if np.all(row == snappedlist[i + 1]):
            delete_list.append(i)
    snappedlist = np.delete(snappedlist, delete_list, axis=0)


    text_file2.write("\n etter snap: \n%s" % snappedlist)
    text_file2.close()

    Pushtodb(snappedlist)
    return "ok"

@app.route('/api', methods=['GET', 'POST'])
def api():
    data = NewDB.getFromDB()
    print(data)
    return json.dumps(data)

@app.route('/login', methods=['POST'])
def login():
    print(request.form.get)
    type_ = request.form.get('type')
    idn = NewDB.loginDB(type_)

    print('New login with id:', idn, " and type", type_)
    return str(idn)

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded = True)
