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
    # print(data.get("tavg"), data.get("wspd"), data.get("tsun"), data.get("prcp"))
    PR = 0.75
    TC = 1 - 0.005 * (data.get("tavg") - 25) if data.get("tavg") is not None else 1
    WC = 1 + 0.01 * math.sqrt(data.get("wspd", 0)) if data.get("wspd", 0) is not None else 1
    SR = data.get("tsun") / 44640 if data.get("tsun") is not None else 1000 / 44640
    PC = math.exp(-data.get("prcp") / 100)
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


# data = get_last_year_weather_data([27.10460180195585, 50.32614931455628], "2003-05-01")
data = {'meta': {'generated': '2024-05-06 21:21:49', 'stations': ['40417', '40415', '40416', '41150']}, 'data': [
    {'date': '2002-06-01', 'tavg': 35.0, 'tmin': 27.2, 'tmax': 42.6, 'prcp': 0.0, 'wspd': None, 'pres': 999.5,
     'tsun': 20940},
    {'date': '2002-07-01', 'tavg': 37.1, 'tmin': 28.7, 'tmax': 45.7, 'prcp': 0.0, 'wspd': None, 'pres': 999.1,
     'tsun': 21240},
    {'date': '2002-08-01', 'tavg': 36.1, 'tmin': 28.5, 'tmax': 44.1, 'prcp': 0.0, 'wspd': None, 'pres': 999.4,
     'tsun': 20820},
    {'date': '2002-09-01', 'tavg': 32.7, 'tmin': 25.1, 'tmax': 41.4, 'prcp': 0.0, 'wspd': None, 'pres': 1006.1,
     'tsun': 18660},
    {'date': '2002-10-01', 'tavg': 29.1, 'tmin': 21.3, 'tmax': 38.5, 'prcp': 0.0, 'wspd': None, 'pres': 1010.9,
     'tsun': 18120},
    {'date': '2002-11-01', 'tavg': 21.4, 'tmin': 15.5, 'tmax': 28.4, 'prcp': 8.0, 'wspd': None, 'pres': 1016.7,
     'tsun': 15780},
    {'date': '2002-12-01', 'tavg': 17.4, 'tmin': 12.9, 'tmax': 22.7, 'prcp': 24.0, 'wspd': None, 'pres': 1018.7,
     'tsun': 10860},
    {'date': '2003-01-01', 'tavg': 15.0, 'tmin': 12.2, 'tmax': 21.7, 'prcp': 10.0, 'wspd': None, 'pres': 1018.7,
     'tsun': 13800},
    {'date': '2003-02-01', 'tavg': 17.9, 'tmin': 12.9, 'tmax': 23.9, 'prcp': 20.0, 'wspd': None, 'pres': 1015.1,
     'tsun': 10860},
    {'date': '2003-03-01', 'tavg': 20.5, 'tmin': 14.7, 'tmax': 27.8, 'prcp': 14.0, 'wspd': None, 'pres': 1013.3,
     'tsun': None},
    {'date': '2003-04-01', 'tavg': 27.1, 'tmin': 20.5, 'tmax': 34.8, 'prcp': 7.0, 'wspd': None, 'pres': 1010.0,
     'tsun': None},
    {'date': '2003-05-01', 'tavg': 32.5, 'tmin': 25.3, 'tmax': 40.3, 'prcp': 0.0, 'wspd': None, 'pres': 1007.1,
     'tsun': 14400}]}


sorted_data_list = sorted(data.get('data'), key=lambda x: int(x['date'][5:7]))
print(sorted_data_list)
# print(data)
area = 1000  # м²
panels_num = get_panels_num(area)

for month in sorted_data_list:
    monthly_production = get_efficiency(panels_num, get_pr_adj(month), month)
    print(f'Ожидаемое производство энергии за {month["date"]} : {round(monthly_production, 2)} kWh')
