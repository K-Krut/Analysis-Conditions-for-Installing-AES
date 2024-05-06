import pandas as pd

from diploma_api.settings import RapidAPI_KEY
from datetime import datetime, timedelta
import requests
import math


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


def get_pr_adj(data):
    PR = 0.75
    TC = 1 - 0.005 * (data["tavg"] - 25)
    WC = 1 + 0.01 * math.sqrt(data["wspd"])
    SR = data["tsun"] / 44640 if data["tsun"] and data["tsun"] is not None else 1
    PC = math.exp(-data["prcp"] / 100)
    return PR * TC * WC * SR * PC


# TODO typical_solar_radiation_for_region
def get_solar_radiation(tsun, days_in_month):
    """
    типичная мощность солнечного излучения в ясный день в полдень составляет 1000 Вт/м²
    :param tsun:
    :param days_in_month:
    :return:
    """
    return (tsun / 60) / 1000 / days_in_month if tsun and tsun is not None else 1000 / days_in_month


def get_panels_num(polygon_area_m2, panel_area=1.6):
    """

    :param polygon_area_m2:
    :param panel_area: panel_area=1.6 м²
    :param area: м²
    :return:
    """
    return polygon_area_m2 / panel_area


def get_efficiency(num_panels, pr_adj, data_, panel_efficiency=0.156):
    """
    в kWh
    радиация в kWh/m²/день
    :param data_:
    :param panel_efficiency:
    :param num_panels:
    :param pr_adj:
    :return:
    """
    days_in_month = pd.to_datetime(data_['date']).days_in_month
    solar_radiation = get_solar_radiation(data_['tsun'], days_in_month)
    return num_panels * panel_efficiency * solar_radiation * pr_adj * days_in_month


# data = get_last_year_weather_data([27.10460180195585, 50.32614931455628], "2024-05-01")
data = {'meta': {'generated': '2024-05-06 18:56:01', 'stations': ['40417', '40415', 'OEJB0', '40416']}, 'data': [
    {'date': '2023-06-01', 'tavg': 36.0, 'tmin': 28.5, 'tmax': 43.7, 'prcp': 0.0, 'wspd': 17.0, 'pres': 1000.9,
     'tsun': None},
    {'date': '2023-07-01', 'tavg': 37.8, 'tmin': 29.5, 'tmax': 46.3, 'prcp': 0.0, 'wspd': 12.9, 'pres': 998.0,
     'tsun': None},
    {'date': '2023-08-01', 'tavg': 37.6, 'tmin': 30.6, 'tmax': 45.8, 'prcp': 0.0, 'wspd': 12.1, 'pres': 1000.0,
     'tsun': None},
    {'date': '2023-09-01', 'tavg': 34.7, 'tmin': 27.0, 'tmax': 43.6, 'prcp': 0.0, 'wspd': 11.2, 'pres': 1003.6,
     'tsun': None},
    {'date': '2023-10-01', 'tavg': 30.5, 'tmin': 23.6, 'tmax': 38.9, 'prcp': 0.7, 'wspd': 11.2, 'pres': 1011.7,
     'tsun': None},
    {'date': '2023-11-01', 'tavg': 23.9, 'tmin': 19.5, 'tmax': 29.3, 'prcp': 24.8, 'wspd': 12.0, 'pres': 1015.8,
     'tsun': None},
    {'date': '2023-12-01', 'tavg': 19.6, 'tmin': 14.3, 'tmax': 26.1, 'prcp': 1.1, 'wspd': 11.0, 'pres': 1018.6,
     'tsun': None},
    {'date': '2024-01-01', 'tavg': 17.7, 'tmin': 13.0, 'tmax': 23.5, 'prcp': 4.1, 'wspd': 17.8, 'pres': 1018.5,
     'tsun': None},
    {'date': '2024-02-01', 'tavg': 17.6, 'tmin': 12.8, 'tmax': 22.8, 'prcp': 25.4, 'wspd': 18.0, 'pres': 1018.4,
     'tsun': None},
    {'date': '2024-03-01', 'tavg': 20.5, 'tmin': 15.2, 'tmax': 26.4, 'prcp': 28.0, 'wspd': 17.9, 'pres': 1015.4,
     'tsun': None},
    {'date': '2024-04-01', 'tavg': None, 'tmin': None, 'tmax': None, 'prcp': None, 'wspd': None, 'pres': None,
     'tsun': None},
    {'date': '2024-05-01', 'tavg': None, 'tmin': None, 'tmax': None, 'prcp': None, 'wspd': None, 'pres': None,
     'tsun': None}]}

print(data)
area = 1000  # м²
print(get_panels_num(area))
monthly_production = get_efficiency(get_panels_num(area), get_pr_adj(data['data'][0]), data['data'][0])
print(f'Ожидаемое производство энергии за июль: {monthly_production} kWh')
