import psycopg2
from config import config

class PsDataModel():
    def __init__(self):
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.parkIds = {}
        except BaseException as err:
            print("Error connecting to db:" + str(err))

    def GetParkId(self, parkName):
        try:
            if parkName in self.parkIds:
                return self.parkIds[parkName]
        
            sql = """SELECT id FROM parkinfo WHERE name = %s"""
            self.cur.execute(sql,(parkName,))
            id = self.cur.fetchall()
            if len(id) == 0:
                return -1
            else:
                return id[0][0]
        except BaseException as err:
            print("Error connecting to db:" + str(err))

    def AddDayInfo(self, dayInfo):
        try:
            checksql = """SELECT id FROM dayinfo WHERE date = %s"""
            self.cur.execute(checksql,(dayInfo.date,))
            id = self.cur.fetchall()
            if len(id) == 0:
                sql = """INSERT INTO dayinfo(date,dow,season) VALUES (%s,%s,%s) RETURNING id"""
                record = (dayInfo.date,dayInfo.dayOfWeek,dayInfo.season)
                self.cur.execute(sql,record)
                id = self.cur.fetchone()[0]
                self.conn.commit()
            else:
                id = id[0][0]
            return id
        except BaseException as err:
            print("Error connecting to db:" + str(err))

    def AddDataPoint(self, dataPoint, dayId):
        try:
            parkId = self.GetParkId(dataPoint.parkName)
            if parkId < 0:
                return
        
            parentsql = """INSERT INTO datapoint(dayid,time,weather,temperature,parkid) VALUES(%s,%s,%s,%s,%s) RETURNING id"""
            childsql = """INSERT INTO ridedatapoint(datapointid,rideid,status,waittime,name) VALUES(%s,%s,%s,%s,%s)"""

            parentrecord = (dayId,dataPoint.time,dataPoint.weather,dataPoint.temperature, parkId)
            self.cur.execute(parentsql,parentrecord)
            id = self.cur.fetchone()[0]

            for ride in dataPoint.rideDataPoints:
                record = (id,ride.id,ride.status,ride.waitTime,ride.name)
                self.cur.execute(childsql,record)
            self.conn.commit()
            return
        except BaseException as err:
            print("Error connecting to db:" + str(err))