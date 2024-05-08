import pandas as pd
from meteostat import Point, Monthly
from diploma_api.settings import RapidAPI_KEY
from datetime import datetime, timedelta
import requests
import math


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


def get_pr_adj(data):
    PR = 0.75
    TC = 1 - 0.005 * (data.get("tavg") - 25) if data.get("tavg") is not None else 1
    WC = 1 + 0.01 * math.sqrt(data.get("wspd", 0)) if data.get("wspd", 0) is not None else 1
    PC = math.exp(-data.get("prcp") / 100) if data.get("prcp") is not None else math.exp(-0 / 100)
    return PR * TC * WC * PC


# TODO typical_solar_radiation_for_region
def get_solar_radiation(tsun):
    """
    типичная мощность солнечного излучения в ясный день в полдень составляет 1000 Вт/м²
    :param tsun:
    :param days_in_month:
    :return: kWh/m²/месяц
    """
    return tsun / 60 if tsun is not None else 1000 / 60


def get_panels_num(polygon_area_m2, panel_area=1.6):
    """

    :param polygon_area_m2:
    :param panel_area: panel_area=1.6 м²
    :return:
    """
    return round(polygon_area_m2 / panel_area)


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
    return num_panels * 1.6 * panel_efficiency * get_solar_radiation(data_['tsun']) * pr_adj


def fill_data(df):
    df['month'] = df.index.month
    df = df.drop(columns=['tmin', 'tmax', 'pres'])
    monthly_means = df.groupby('month').transform(lambda x: x.fillna(x.mean()))
    for column in df.columns:
        if column not in ['month']:
            df[column] = df[column].fillna(monthly_means[column]).fillna(0)
    df = df.drop(columns=['month'])
    df['date'] = [str(x[0])[0:10] for x in df.to_records()]
    return df.to_dict('records')


# data = get_last_year_weather_data([27.10460180195585, 50.32614931455628], [2023, 5])
# print(data)
# area = 20  # м²
# panels_num = get_panels_num(area)
# filled_data = fill_data(data)
# annualy = 0
# print(panels_num * 1.6)
# for month in filled_data[-12:]:
#     monthly_production = get_efficiency(panels_num, get_pr_adj(month), month)
#     annualy += monthly_production
#     print(f'{month["date"]} : {round(monthly_production, 2)} kWh')
#
# E = 20 * 15 * 1250 * 0.75
#
# print(E / 100)
# print(annualy)


