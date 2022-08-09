import json
import requests
from dateutil.parser import parse
from datetime import datetime

class WeatherAPI(object):

    def __init__(self):
        self.APIBase = "https://api.openweathermap.org/data/2.5/weather?lat="
        self.APIKey = "daaf8054c694ebba0318c7c9cb3ab954"
        self.previousData = []


    def GetWeather(self, lat, long):
        matching = self.GetPrevious(lat,long)

        if matching:
            return (matching[3],matching[4])
        else:
            data = self.GetDataFromAPI(lat, long)
            self.previousData.append((lat,long,datetime.utcnow(),data[0],data[1]))
            return data


    def GetPrevious(self, lat, long):
        self.ClearOldData()

        for item in self.previousData:
            if item[0] - 1 < lat and item[0] + 1 > lat:
                if item[1] - 1 < long and item[1] + 1 > long:
                    return item


    def ClearOldData(self):
        upToDate = []
        for item in self.previousData:
            difference = datetime.utcnow() - item[2]
            if difference.seconds < 6000:
                upToDate.append(item)

        self.previousData = upToDate

    def GetDataFromAPI(self, lat, long):
        url = self.APIBase + str(lat) + "&lon=" + str(long) + "&appid=" + self.APIKey
        response = requests.get(url)
        weather = -1
        temp = -1
        
        if response.status_code == 200:
            data = response.content
            jsonData = json.loads(data)
            weather = jsonData["weather"][0]["id"]
            temp = jsonData["main"]["temp"]

        return (weather,temp)