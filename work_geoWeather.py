#!/usr/bin/python3
import requests
import json
from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut
#from pyowm import OWM
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import ssl

openWeatherApi = "e09577237978b0a40fffd3ec2597617a"

class Weather:

  def __init__(self):
    # get Ip, region etc by url
    self.ipInfoUrl = 'https://ipinfo.io/'
    context = ssl._create_unverified_context()
    self.html = urllib.request.urlopen(self.ipInfoUrl, context=context).read()
    self.soup = BeautifulSoup(self.html, 'html.parser')

    self.data = json.loads(self.html)
    self.userIp = self.data["ip"]
    self.userRegion = self.data["region"]

    #geopy - get latitude, longitude
    self.wantedCity = "seoul"
    self.geolocator = Nominatim(user_agent="soos")

  def geopyLatLonWeather(self,wantedCity):
    self.wantedCity = wantedCity
    #self.wantedCity = str(input("City?"))
    try:
        self.location = self.geolocator.geocode(self.wantedCity, timeout = 10)
        self.lat = str(self.location.latitude)
        self.lon = str(self.location.longitude)
        self.latLonUrl = f"http://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={openWeatherApi}"
        context = ssl._create_unverified_context()
        url = urllib.request.urlopen(self.latLonUrl, context=context)
        apid = url.read()
        data = json.loads(apid)
        city = data['name']
        weather = data['weather'][0]['main']
        temp = int(data['main']['temp'] - 273.15)
        showText = f"_______________ in {city} ___ {weather}, {temp}˚C"
        print(showText)
        return showText
    except GeocoderTimedOut as e:
        showText = ""
        showText = e
    finally:
        return showText

  def urlIpRegionWeather(self):
    try:
        self.ipRegionUrl = f"https://api.openweathermap.org/data/2.5/weather?q={self.userRegion}&appid={openWeatherApi}"
        context = ssl._create_unverified_context()
        url = urllib.request.urlopen(self.ipRegionUrl, context=context)
        apid = url.read()
        data = json.loads(apid)
        city = data['name']
        weather = data['weather'][0]['main']
        temp = int(data['main']['temp'] - 273.15)
        showText = f"___ The weather in {city} ___ {weather}, {temp}˚C"
        print(showText)
        return showText
    except GeocoderTimedOut as e:
        showText = ""
        showText = e
    finally:
        return showText
"""
if __name__ == '__main__':
    Weather().geoTypeWeather()

{'coord': {'lon': 126.98, 'lat': 37.57},
'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}],
'base': 'stations', 'main': {'temp': 296.8, 'feels_like': 298.48, 'temp_min': 295.15, 'temp_max': 298.15, 'pressure': 1006, 'humidity': 78},
 'visibility': 6000, 'wind': {'speed': 2.6, 'deg': 300},
 'clouds': {'all': 100}, 'dt': 1592311757,
 'sys': {'type': 1, 'id': 8105, 'country': 'KR', 'sunrise': 1592251822, 'sunset': 1592304916}, 'timezone': 32400, 'id': 1835848,
 'name': 'Seoul', 'cod': 200}
"""
