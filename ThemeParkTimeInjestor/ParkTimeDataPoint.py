from dataclasses import dataclass
from enum import Enum
from typing import List
import datetime

class Season(Enum):
    WINTER = 0
    SPRING = 1
    SUMMER = 2
    FALL = 3

class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Status(Enum):
    OPEN = 0
    DELAYED = 1
    CLOSED = 2

class Holiday(Enum):
    ISHOLIDAY = 0
    NEARHOLIDAY = 1
    NOTHOLIDAY = 2

@dataclass
class RideDataPoint:
    id: str=None
    name: str=None
    status: int=None
    waitTime: int=None

@dataclass
class ParkTimeDataPoint:
    parkName: str=None
    date: str=None
    dayOfWeek: int=None
    season: int=None
    time: str=None
    weather: int=None #Uses OpenWeatherMap codes https://openweathermap.org/current
    temperature: int=None #Uses kelvin
    rideDataPoints: List[RideDataPoint] = None

@dataclass
class ParkMetaData:
    parkName: str=None
    parkId: str=None
    isOpen: bool=False
    openTime: datetime=None
    closeTime: datetime=None
    lat: float=0
    long: float=0