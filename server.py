import time
import json
import snap


from flask import *
app = Flask(__name__)
GlobalList = []




def Pushtodb(Snappedlist):
    print("pushed to DB")

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
    if (len(GlobalList) > 10):
        print("multiple entries:")
        print(GlobalList)
        Snappedlist = snap.snap_to_road(GlobalList, True)
        print("new:")
        print(Snappedlist)
        GlobalList = []
        Pushtodb(Snappedlist)
    return "ok"

if __name__ == "__main__":
  #  app.run(host='0.0.0.0', threaded=True)
    app.run(host='0.0.0.0', port=33)

