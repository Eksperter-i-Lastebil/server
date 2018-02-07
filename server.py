import time
import json
import snap

GlobalList = []

from flask import *
app = Flask(__name__)
GlobalList = []




@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/events', methods=['POST'])
def events():
    print(request.form.get)
    print("\n \n New POST request... \n")
    dummyList = [request.form.get('id'),request.form.get('lat'),request.form.get('lng'), request.form.get('time')]
    print("dummy:", dummyList)
    global GlobalList
    GlobalList.append(dummyList)
    if (len(GlobalList) > 1):
        print("multiple entries:")
        print(GlobalList)
        Snappedlist = snap.snap_to_road(GlobalList, True)
        print("new:")
        print(Snappedlist)
        GlobalList = []

        #pushToDB
    return "ok"


def MarkusFunc():
    if ShouldSend(): ## hvis over gitt antall punkt


        print("sender til snap...")
        '''
        sender:
        [[id, lat, lng, time]]
         [id, lat, lng, time]]
        ##
        mottar:
        [[id, lat, lng, time]
        [id, lat, lng, time]
        [id, lat, lng, time]]

        pushToDB() ->
    else:
        print("avventer")
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)

