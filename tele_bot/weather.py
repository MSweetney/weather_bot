from datetime import datetime
import requests

from .config import WEATHER_TOKEN


# Weather forecast functions
def get_current_weather(city):
    data = get_weather_data(city)
    current = data['current']
    cur_temp = round(current['temp'])
    cur_wind_deg = wind_direction(current['wind_deg'])
    cur_wind_sp = round(current['wind_speed'], 1)
    ans = (f'Current weather in {city} is {cur_temp} celsius. \n' +
           f'Wind is {cur_wind_deg} {cur_wind_sp} m/s')
    return ans


def get_daily_forecast(city):
    data = get_weather_data(city)
    ans = ''
    daily = data['daily']
    for day in daily:
        day_date = day['dt']
        date = datetime.utcfromtimestamp(day_date).strftime('%d %b')
        day_temp = round(day['temp']['day'])
        ans += f'{date}\t{day_temp} degrees\n'
    return ans


def get_weather_data(city):
    cities = {
        'Moscow': [55.75, 37.62],
        'Saint-Petersburg': [59.93, 30.30],
        'Yalta': [44.50, 34.16],
        'Istanbul': [41.01, 28.97]
    }

    lat = cities[city][0]
    lon = cities[city][1]
    part = 'minutely,alerts'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={units}&exclude={part}&appid={WEATHER_TOKEN}'
    data = requests.get(url).json()
    return data


def wind_direction(deg):
    wind = ''
    if 335 <= deg <= 360 or 0 <= deg <= 25:
        wind = 'N'
    elif 295 <= deg < 335:
        wind = 'NW'
    elif 245 <= deg < 295:
        wind = 'W'
    elif 205 <= deg < 245:
        wind = 'SW'
    elif 155 <= deg < 205:
        wind = 'S'
    elif 115 <= deg < 155:
        wind = 'SE'
    elif 65 <= deg < 115:
        wind = 'E'
    elif 25 <= deg < 65:
        wind = 'NE'
    return wind

    # Weather forecast functions end