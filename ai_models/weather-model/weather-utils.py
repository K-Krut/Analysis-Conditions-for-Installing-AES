from diploma_api.settings import RapidAPI_KEY
from datetime import datetime, timedelta
import requests


def get_date_start(date_end):
    previous_date = datetime.strptime(date_end, '%Y-%m-%d') - timedelta(days=30 * 11)
    return previous_date.replace(day=1).strftime('%Y-%m-%d')


def get_last_year_weather_data(coordinates, date_end):
    response = requests.get(
        "https://meteostat.p.rapidapi.com/point/monthly",
        headers={
            "X-RapidAPI-Key": RapidAPI_KEY,
            "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
        },
        params={
            "lat": coordinates[0],
            "lon": coordinates[1],
            "start": get_date_start(date_end),
            "end": date_end,
        }
    )

    return response.json()
