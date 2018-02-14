from tinydb import TinyDB, Query, where
from tinydb.operations import delete
import tinydb.operations
import time
from tinyrecord import transaction
import json

Pos       = Query()
db_all    = TinyDB('db.json')
db_points = db_all.table('points')
db_trips  = db_all.table('trips')

def db_insert(idn, latitude, longitude, timestamp):
    with transaction(db_points) as tr:
        tr.insert({'id' : idn, 'lat' : latitude, 'lng' : longitude, 'time' : timestamp})

def db_newtrip(plowtype):
    # with transaction(db_trips) as tr:
    idn = str(db_trips.insert({'type' : plowtype}))
    return idn

def db_getpoints():
    data = []
    for trip in db_trips.all():
        item = trip
        item["points"]=db_gettrip(trip.get('id'))
        data.append(item)

    return (json.dumps(data))

def db_gettrip(trip_id):
    return (db_points.search(Pos.id == trip_id))
