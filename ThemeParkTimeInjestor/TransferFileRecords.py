import json
import glob
import os
from PostgresDataModel import PsDataModel
from ParkTimeDataPoint import *


def LoadObjects(path):
    dataPoints = []
    files = glob.glob(os.path.join(path,"*.txt"))

    for file in files:
        with open(file, 'r') as f:
            for line in f:
                dataPoint = json.loads(line)
                dataPoints.append(dataPoint)
    return dataPoints



def SaveObjects(dataPoints):
    dataModel = PsDataModel()
    dateIds = {}
    for dataPoint in dataPoints:
        if dataPoint['date'] in dateIds:
            dateId = dateIds[dataPoint['date']]
        else:
            dayInfo = ParkTimeDataPoint()
            dayInfo.date = dataPoint['date']
            dayInfo.dayOfWeek = dataPoint['dayOfWeek']
            dayInfo.season = dataPoint['season']
            dateId = dataModel.AddDayInfo(dayInfo)
            dateIds[dataPoint['date']] = dateId

        parkDataPoint = ParkTimeDataPoint()
        parkDataPoint.parkName = dataPoint['parkName']
        parkDataPoint.time = dataPoint['time']
        parkDataPoint.weather = dataPoint['weather']
        parkDataPoint.temperature = dataPoint['temperature']
        parkDataPoint.rideDataPoints = []
        for rdp in dataPoint['rideDataPoints']:
            point = RideDataPoint()
            point.id = rdp['id']
            point.status = rdp['status']
            point.waitTime = rdp['waitTime']
            point.name = rdp['name']
            parkDataPoint.rideDataPoints.append(point)

        dataModel.AddDataPoint(parkDataPoint,dateId)

def main():
    print("Starting transfer")
    #S:/Users/andre/Desktop/ThemeParkInjestorOutput
    path = input("Enter path to data folder: ")#S:/Projects/Programming Projects/ThemeParkWaitTimes/ThemeParkTimeInjestor/TestOutput
    dataPoints = LoadObjects(path)
    SaveObjects(dataPoints)



if __name__ == '__main__':
    main()
