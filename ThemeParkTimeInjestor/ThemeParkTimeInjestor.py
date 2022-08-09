##TODO
#Use the api from pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
#Find a method to get the weather
#Find a method to get holidays
#Define the object structure for each timestamp
#   date, day of week, season, time, weather, temp, status, wait time, isHoliday(yes, no, near)
#Save data to file
#Save very 30 min?
#Set to not run when the park is closed (Need to get hours from api)
#Keep seperate records for each park



##Steps
#On startup query for park hours
#Start timer that will cycle every half hour on the half hour
#   Check if hours are for current day, if no then update
#   Check if within hours
#       Get weather
#       Get park times
#       Get holiday status (compare to static file?)
#       Save information to file(s)

from ParkTimeDataPoint import *
from RepeatedTimer import *
from ThemeParkAPI import *
from WeatherAPI import *
import os
import json
from dateutil.parser import parse
from datetime import datetime
import pytz
import pickle

class ThemeParkTimeInjestor:

    def __init__(self, filePath):
        self.ThemeParkAPI = ThemeParkAPI()
        self.WeatherAPI = WeatherAPI()
        self.tz = pytz.timezone("US/Arizona")
        self.filePath = filePath
        self.parks = self.LoadParks()
        self.SetDayInfo()

    def LoadParks(self):
        parks = []
        filePath = os.path.join(self.filePath,"parks.json")
        with open(filePath, 'r') as j:
            parksraw = json.loads(j.read())
        
        for parkRaw in parksraw:
            park = ParkMetaData()
            park.parkId = parkRaw["id"]
            park.parkName = parkRaw["name"]
            park.lat = parkRaw["lat"]
            park.long = parkRaw["long"]
            parks.append(park)
        
        print("Processing " + str(len(parks)) + " parks")
        return parks

    def SetDayInfo(self):
        self.masterDataPoint = ParkTimeDataPoint()
        self.masterDataPoint.date = str(datetime.now(tz=self.tz))
        self.masterDateCode = self.GetDateCode(datetime.now(tz=self.tz))
        self.masterDataPoint.dayOfWeek =datetime.now(tz=self.tz).weekday()
        self.masterDataPoint.season = self.GetSeason()
        for park in self.parks:
            self.ThemeParkAPI.GetOpeningHours(park)

    def StartDataCollection(self):
        self.rt = RepeatedTimer(1800,self.CollectData)
        self.CollectData()

    def EndDataCollection(self):
        if self.rt:
            self.rt.stop()

    def CollectData(self):
        if self.GetDateCode(datetime.now(tz=self.tz)) > self.masterDateCode:
            self.SetDayInfo()

        dataPoints = []
        for park in self.parks:
            if park.isOpen and datetime.now(tz=self.tz) > park.openTime and datetime.now(tz=self.tz) < park.closeTime:
                weather, temp = self.WeatherAPI.GetWeather(park.lat,park.long)

                attractionData = self.ThemeParkAPI.GetAttractionData(park)
                rideDataPoints = self.GetRideTimes(park, attractionData)

                parkDataPoint = ParkTimeDataPoint()
                parkDataPoint.parkName = park.parkName
                parkDataPoint.date = self.masterDataPoint.date
                parkDataPoint.dayOfWeek = self.masterDataPoint.dayOfWeek
                parkDataPoint.season = self.masterDataPoint.season
                parkDataPoint.time = str(datetime.now(tz=self.tz))
                parkDataPoint.weather = weather
                parkDataPoint.temperature = temp
                parkDataPoint.rideDataPoints = rideDataPoints 
                dataPoints.append(parkDataPoint)

        self.SaveData(dataPoints)
        if len(dataPoints) > 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M") + ": Saved " + str(len(dataPoints)))
        else:
            closedCount = sum(p.isOpen == False for p in self.parks)
            outOfHoursCount = len(self.parks) - closedCount
            print(datetime.now().strftime("%Y-%m-%d %H:%M") + ": No parks currently open (" + str(closedCount) + " closed, " + str(outOfHoursCount) + " out of hours)")

    def SaveData(self, dataPoints):
        suffix = ".txt"
        for point in dataPoints:
            filePath = os.path.join(self.filePath,point.parkName + suffix)
            with open(filePath, 'a') as f:
                jsonString = json.dumps(point, default=self.serialize) + "\n"
                f.write(jsonString)

    def GetDateCode(self, date):
        return 10000*date.year + 100*date.month + date.day

    def GetSeason(self):
        doy = datetime.today().timetuple().tm_yday

        # "day of year" ranges for the northern hemisphere
        spring = range(80, 172)
        summer = range(172, 264)
        fall = range(264, 355)
        # winter = everything else

        if doy in spring:
            season = 1
        elif doy in summer:
            season = 2
        elif doy in fall:
            season = 3
        else:
            season = 0
        return season

    def GetRideTimes(self, park, liveJson):
        results = []
        for item in liveJson:
            if "queue" in item and item["entityType"] == "ATTRACTION":
                results.append(self.CreateDatePoint(park,item))
        return results


    def CreateDatePoint(self, park, attractionJson):
        point = RideDataPoint()
        point.id = attractionJson["id"]
        point.name = attractionJson["name"]
        if attractionJson["status"] == "OPERATING":
            point.status = 0
        if attractionJson["status"] == "DOWN":
            point.status = 1
        if attractionJson["status"] == "CLOSED":
            point.status = 2

        if "STANDBY" in attractionJson["queue"]:
            point.waitTime = attractionJson["queue"]["STANDBY"]["waitTime"]
            if not point.waitTime:
                point.waitTime = 0
        else:
            point.waitTime = -1
        return point

    def serialize(self, obj):

        return obj.__dict__