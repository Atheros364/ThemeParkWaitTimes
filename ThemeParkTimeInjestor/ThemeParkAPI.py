import json
import requests
from ParkTimeDataPoint import *
from dateutil.parser import parse
from datetime import datetime

class ThemeParkAPI(object):

	def __init__(self):
		self.APIBase = "https://api.themeparks.wiki/v1/entity/"

	#get opening hours
	def GetOpeningHours(self, parkDataPoint):
		getHoursApi = "/schedule"
		today = datetime.now()
		currentDateCode = 10000*today.year + 100*today.month + today.day

		try:
			url = self.APIBase + parkDataPoint.parkId + getHoursApi
			response = requests.get(url)

			if response.status_code == 200:
				jsonResponse = response.json()

				schedule = jsonResponse["schedule"]
				if schedule:
					for item in schedule:
						dateString = item["date"]
						date = parse(dateString)
						dateCode  = 10000*date.year + 100*date.month + date.day

						if dateCode > currentDateCode:
							break

						if dateCode == currentDateCode and item["type"] == "OPERATING":
							parkDataPoint.isOpen = True
							parkDataPoint.openTime = parse(item["openingTime"])
							parkDataPoint.closeTime = parse(item["closingTime"])
							return

		except:
			print("Error calling opening hours api")


	#get wait times
	def GetAttractionData(self, parkDataPoint):
		getDataApi = "/live"

		try:
			url = self.APIBase + parkDataPoint.parkId + getDataApi
			response = requests.get(url)

			if response.status_code == 200:
				jsonResponse = response.json()

				result = jsonResponse["liveData"]
				return result

		except:
			print("Error calling live data api")