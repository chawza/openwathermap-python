# Weather App
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