"""
TItle: Weather Forecast news Application
Author: Nabeel Kahlil Maulana
github: https://github.com/chawza/openwathermap-python

This program will show openwathermap.org weather forcast on cli interface. It request an API endpoint to retrieve
list of 5 upcoming days weather forecast.

In order to minimalize the program, it does not use any external library. Only standard library is used.
It uses `@dataclass` to store the data strcture and `urllib` to handle the api request.

## HOW TO USE
before use, set your machine environment variable WEATHER_API before excecuting the program. Please visit https://openweathermap.org/api
for more information.
  
  on linux: `export WEATHER_API=<YOUR_API>`
  on windows: `set WEATHER_API=<YOUR_API>`

to run the program, use python3 to use this command
`python weather.py`

## Important Note
- it only show the first 3 hour of day cylce on each day
- use `fetch_and_save_forcast()` function to save the data, then use `load_locale` to load the saved data.

"""

from urllib.request import urlopen
from urllib.parse import urlencode
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Forecast:
  dt: datetime 
  temp: str

  def get_date_text(self):
    strftime_pattern = '%a, %d %b %Y'
    text = self.dt.strftime(strftime_pattern)
    return text
  
  def get_day(self):
    return self.dt.day

def fetch_data(url):
  with urlopen(url) as res:
    body = res.read().decode('utf-8')
  return json.loads(body)

def fetch_and_save_forcast(url, filepath='./test.json'):
  weather_data = fetch_data(url)
  with open(filepath, 'w') as f:
    text = json.dumps(weather_data)
    f.write(text)

def load_locale(filepath='./test.json'):
  with open(filepath, 'r') as f:
    data = f.read()
  return json.loads(data)

def show_forecast(forcasts: List[Forecast]):
  print('Weather Forecast:')
  degree_char = chr(176)
  for forcast in forcasts:
    txt = f'{forcast.get_date_text()}: {forcast.temp} {degree_char}C'
    print(txt)

def process_weather_data(weather_list) -> List[Forecast]:
  forcasts = [] 
  for weather in weather_list:
    forcasts.append(Forecast(
      dt = datetime.fromtimestamp(weather['dt']),
      temp = weather['main']['temp']
    ))
  return forcasts 

def filter_data_per_day(weather_list: List[Forecast]):
  weather_list.sort(key=lambda x : x.dt)

  day_list = []
  forcasts = []
  for forcast in weather_list:
    if forcast.get_day() not in day_list:
      day_list.append(forcast.get_day())
      forcasts.append(forcast)

  return forcasts

def main(API):
  base_url = f'http://api.openweathermap.org/data/2.5/forecast' # https://openweathermap.org/forecast5
  # Jakarta latitude and Longtitude: https://www.latlong.net/place/jakarta-indonesia-27575.html
  params = {
    'appid': API,
    'lat': -6.200000,
    'lon':  106.816666,
    'units': 'metric'
  }
  query = urlencode(params)
  url = f'{base_url}?{query}'

  api_response = fetch_data(url)
  # api_response = load_locale()
  weather_list = api_response['list']

  forcasts = process_weather_data(weather_list)
  forcasts = filter_data_per_day(forcasts)
  show_forecast(forcasts)

if __name__ == '__main__':
  import os
  openwheater_API = os.environ.get('WEATHER_API')
  if openwheater_API is None:
    print('openwheathermap.org API key is required. please visit : https://openweathermap.org/api')
  else:
    main(openwheater_API)
  # test()