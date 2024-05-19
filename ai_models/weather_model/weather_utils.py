import random
from builtins import print

from meteostat import Point, Monthly
from diploma_api.settings import RapidAPI_KEY
from datetime import datetime, timedelta
import requests
import math

PANEL_SIZE = 1.6  # м²
PANEL_EFFICIENCY = 0.156  # 15.6%


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
    WC = 1 + 0.01 * math.sqrt(data.get("wspd")) if data.get("wspd") is not None else 1
    PC = math.exp(-data.get("prcp") / 100) if data.get("prcp") is not None else 1
    index = PR * TC * WC * PC
    return index if index >= 0.5 else 0.5


# TODO typical_solar_radiation_for_region
def get_solar_radiation(tsun, month):
    """
    типичная мощность солнечного излучения в ясный день в полдень составляет 1000 Вт/м²
    :param month:
    :param tsun:
    :param days_in_month:
    :return: kWh/m²/месяц
    """
    solar_radiation_ukraine = {
        1: 200,
        2: 220,
        3: 303,
        4: 316,
        5: 350,
        6: 345,
        7: 350,
        8: 335,
        9: 250,
        10: 300,
        11: 250,
        12: 170
    }
    hours = solar_radiation_ukraine[month]
    return tsun / 60 if tsun not in [None, 0] else random.randint(hours, hours + 5)


def get_panels_num(polygon_area_m2, panel_area=PANEL_SIZE):
    """
    :param polygon_area_m2:
    :param panel_area: panel_area=1.6 м²
    :return:
    """
    return round(polygon_area_m2 / panel_area)


def get_efficiency(num_panels, pr_adj, data_, panel_efficiency=PANEL_EFFICIENCY):
    """
    в kWh
    радиация в kWh/m²/месяц
    :param data_:
    :param panel_efficiency:
    :param num_panels:
    :param pr_adj:
    :return:
    """
    solar = get_solar_radiation(data_['tsun'], data_['month'])
    print(data_['month'], '  -  ', num_panels, PANEL_SIZE, panel_efficiency, solar, pr_adj)
    return num_panels * PANEL_SIZE * panel_efficiency * solar * pr_adj


def fill_data(df):
    df['month'] = df.index.month
    df = df.drop(columns=['tmin', 'tmax', 'pres'])
    monthly_means = df.groupby('month').transform(lambda x: x.fillna(x.mean()))
    for column in df.columns:
        if column not in ['month']:
            df[column] = df[column].fillna(monthly_means[column]).fillna(0)
    df['date'] = [str(x[0])[0:10] for x in df.to_records()]
    return df.to_dict('records')


def generate_solar_stats_result(monthly_weather_data, panels_num):
    monthly_data = [
        {
            "date": month.get('date'),
            "energy": round(get_efficiency(panels_num, get_pr_adj(month), month))  # kWh
        }
        for month in monthly_weather_data
    ]
    monthly_data = sorted(monthly_data, key=lambda x: int(x['date'][5:7]))
    return {
        "panels": panels_num,
        "panels_area": panels_num * PANEL_SIZE,
        "panels_efficiency": PANEL_EFFICIENCY,
        "month_energy_stats": monthly_data,
        "yearly_energy": sum([x.get("energy") for x in monthly_data])
    }


def get_solar_energy_output_stats(coordinates, area):
    today = datetime.now()
    weather_stats_data = get_last_year_weather_data(coordinates, [today.year - 1, today.month])
    filled_data = fill_data(weather_stats_data)
    return generate_solar_stats_result(filled_data[-12:], get_panels_num(area))



