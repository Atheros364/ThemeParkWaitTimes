import psycopg2
import psycopg2.extras
import logging
from config import config

class PsDataModel():

    def __init__(self):
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            self.parkIds = {}
        except BaseException as err:
            logging.error("Error connecting to db:" + str(err))

    def GetAllDataForPark(self, parkName):
        try:
            # Get park Id
            sql = """SELECT id FROM parkinfo WHERE name = %s"""
            self.cur.execute(sql,(parkName,))
            parkId = self.cur.fetchall()[0]['id']

            # Get park graph info
            sql = """SELECT ridegraph FROM parkinfo WHERE name = %s"""
            self.cur.execute(sql,(parkName,))
            parkGraph = self.cur.fetchall()[0]['ridegraph']

            # Get all ridedatapoints with day and time info
            sql = """SELECT dayinfo.date, dayinfo.dow, dayinfo.season, dayinfo.holiday, datapoint.time, datapoint.weather, datapoint.temperature, ridedatapoint.rideid, ridedatapoint.status, ridedatapoint.waittime
FROM ridedatapoint JOIN datapoint ON ridedatapoint.datapointid = datapoint.id
JOIN dayinfo ON dayinfo.id = datapoint.dayid
WHERE parkid = parkId"""
            self.cur.execute(sql,(parkName,))
            datapoints = self.cur.fetchall()

            return datapoints, parkGraph

        except BaseException as err:
            logging.error("Error getting data points:" + str(err))