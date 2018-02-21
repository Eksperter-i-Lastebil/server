from tinydb import TinyDB, Query, where
from tinydb.operations import delete, add
import tinydb.operations
import time
from tinyrecord import transaction
import json

Pos = Query()
db_all = TinyDB('db.json')
db_points = db_all.table('points')
db_trips  = db_all.table('trips')

Oldtime = 600480 #1 Week

def db_insert(idn, latitude, longitude, timestamp):
    with transaction(db_points) as tr:
        tr.insert({'id' : idn, 'lat' : latitude, 'lng' : longitude, 'time' : timestamp})

def db_newtrip(plowtype):
    idn = db_trips.insert({'type' : plowtype})
    db_trips.update({'id':str(idn)}, doc_ids=[idn])
    return idn

def db_getpoints():
    data = []
    for trip in db_trips.all():
        item = trip
        item["points"]=db_gettrip(trip.get('id'))
        if item["points"] != []:
            data.append(item)

    return (json.dumps(data))

def db_getnewest(idn):
    points = db_points.search(Pos.id == idn)
    if not points:
        return None
    else:
        return (json.dumps(points[-1]))

def db_gettrip(trip_id):
    return (db_points.search((Pos.id == trip_id) & (Pos.time > str(time.time()-Oldtime))))
