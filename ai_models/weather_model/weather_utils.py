from meteostat import Point, Monthly, Daily, Hourly
from diploma_api.settings import RapidAPI_KEY
from datetime import datetime, timedelta
import requests


def get_date_start(date_end):
    previous_date = datetime.strptime(date_end, '%Y-%m-%d') - timedelta(days=30 * 11 * 20)
    return previous_date.replace(day=1).strftime('%Y-%m-%d')


def get_last_year_weather_data_api(coordinates, date_end, date_start="2000-01-01"):
    response = requests.get(
        "https://meteostat.p.rapidapi.com/point/monthly",
        headers={
            "X-RapidAPI-Key": RapidAPI_KEY,
            "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
        },
        params={
            "lat": coordinates[0],
            "lon": coordinates[1],
            "start": date_start,
            "end": date_end,
        }
    )
    print(response.status_code)
    print(response.text)

    return response.json()


def get_last_year_weather_data(coordinates, de, ds=[2000, 1]):
    data_fetch = Monthly(
        Point(coordinates[1], coordinates[0]),
        start=datetime(ds[0] if ds and ds[0] else 2000, ds[1] if ds and ds[1] else 1, 1),
        end=datetime(de[0], de[1], 1)
    )
    return data_fetch.fetch()


def get_daily_weather_stats(coordinates, end, st=[2020, 1, 1]):
    data_fetch = Daily(
        Point(coordinates[1], coordinates[0]),
        start=datetime(st[0], st[1], st[2]),
        end=datetime(end[0], end[1], end[2]) if end else datetime(2024, 1, 1)
    )
    return data_fetch.fetch()


def get_hourly_weather_data(coordinates, ds, de):
    data_fetch = Hourly(
        Point(coordinates[1], coordinates[0]),
        start=datetime(ds[0], ds[1], 1),
        end=datetime(de[0], de[1], 1)
    )
    return data_fetch.fetch()

