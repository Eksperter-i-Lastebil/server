
from flask_cors import CORS


import time
from flask import *
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'test'
app.config['MYSQL_DATABASE_DB'] = 'eitlastebil'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
CORS(app)

def loginDB(plowtype):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO trips (egenskap) VALUES (%s)"
    data = plowtype
    cursor.execute(sql,data)
    conn.commit()
    id = cursor.lastrowid
    return id

def insertToDb(idn, latitude, longitude, timestamp):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO positions (lat, lng, time, TripID) VALUES (%s, %s, %s, %s)"
    data = (latitude, longitude, timestamp, idn)
    cursor.execute(sql, data)
    conn.commit()

def getFromDB():
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * FROM trips WHERE DATE_SUB(CURDATE(),INTERVAL 7 DAY) <= startTime;"
    cursor.execute(query)
    results = cursor.fetchall()
    returnArray = []
    for trip in results:
        query = ("SELECT lat,lng,time FROM positions WHERE TripID = "+ str(trip[0]))
        cursor.execute(query)
        posInTrip = cursor.fetchall()
        newTime = time.mktime(trip[2].timetuple())
        returnArray.append({
            'type':trip[1],
            'time':newTime,
            'points':[{'lat':point[0], 'lng':point[1], 'time':point[2]} for point in posInTrip]
        })
    return returnArray


## MYSQL - QUERY ##
# just in case we need to drop DB and start over
'''
CREATE DATABASE `eitlastebil`

CREATE TABLE `trips` (
	`idTrip` INT(11) NOT NULL AUTO_INCREMENT,
	`egenskap` VARCHAR(50) NOT NULL,
	`startTime` TIMESTAMP NOT NULL DEFAULT '',
	PRIMARY KEY (`idTrip`)
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

CREATE TABLE `positions` (
	`idPos` INT(11) NOT NULL AUTO_INCREMENT,
	`lat` VARCHAR(50) NOT NULL DEFAULT '0',
	`lng` VARCHAR(50) NOT NULL DEFAULT '0',
	`time` VARCHAR(50) NOT NULL DEFAULT '0',
	`TripID` INT(11) NULL DEFAULT NULL,
	PRIMARY KEY (`idPos`),
	INDEX `TripKey` (`TripID`),
	CONSTRAINT `TripKey` FOREIGN KEY (`TripID`) REFERENCES `trips` (`idTrip`)
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

'''