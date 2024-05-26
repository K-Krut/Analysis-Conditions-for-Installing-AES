import uuid
import boto3
import numpy as np
from io import BytesIO
from matplotlib import pyplot as plt
from ai_models.weather_model.weather_utils import get_hourly_weather_data
from diploma_api.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME


WIND_TURBINE_AREA = 0.0144  # км², для турбины с лопастями 50м

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)


def weather_for_wind_calculation(coords, ds, de):
    df = get_hourly_weather_data(coords, ds, de)
    df = df.drop(columns=['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'pres', 'tsun', 'coco', 'wpgt'])
    df['month'] = df.index.month
    df['hour'] = [str(x[0])[11:16] for x in df.to_records()]
    return df.groupby('month')  # return df.to_records()  # ['wdir', 'wspd', 'month', 'hour']


def generate_presigned_url(object_key, expiration=3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': object_key},
        ExpiresIn=expiration
    )


def draw_wind_rose(records, month):
    data = np.array(records, dtype=[('wdir', float), ('wspd', float), ('time', 'U5')])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.bar(np.radians(data['wdir']), data['wspd'], width=0.1, bottom=0.1)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    bucket_path = f"wind-roses/wind-rose-{month}-{uuid.uuid4()}.png"
    s3_client.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=bucket_path, Body=buf, ContentType='image/png')
    buf.close()
    plt.close(fig)
    return generate_presigned_url(bucket_path)


def get_wind_rose_for_year(yearly_weather_data):
    for name, group in yearly_weather_data:
        group = group.drop(columns=['month'])
        draw_wind_rose(group.to_records(index=False), name)


def get_wind_speeds(yearly_weather_data):
    speeds = {}
    for month, group in yearly_weather_data:
        speeds[month] = group['wspd'].to_numpy()
    return speeds


def get_power(wind_speeds, r=50):  # Vestas V112-3.45 MW - 54,6 m
    """
    :param wind_speeds:
    :param r: R is the radius of the rotor (in meters, m)
    rho - denotes the air density (in kilograms per cubic meter, kg/m³).
    A - is the swept area (in square meters, m²)
    Cp stands for the power coefficient, represents the efficiency of the wind turbine in capturing the wind’s energy
    :return:
    """
    rho = 1.225
    A = np.pi * (r ** 2)
    Cp = 0.4
    return (0.5 * rho * A * ((wind_speeds / 3.6) ** 3) * Cp * 0.9) / 1000


def get_num_of_wind_turbins(area):
    return area / WIND_TURBINE_AREA


def get_wind_energy_output(wind_speeds, turbines_num):
    p = sum(get_power(wind_speeds))

#
# # coord = [26.245628498478002, 50.340760265673204]
# coord = [35.2577876585286, 47.74093953469412]
#
# data_weather = weather_for_wind_calculation(coord, [2023, 11], [2024, 1])
# # for i, j in data_weather:
# #     print(i)
# # for k in j.to_records():
# #     print(str(k[0])[0:16], k[2])
#
# get_wind_rose_for_year(data_weather)
#



# winds = get_wind_speeds(data_weather)
# res = 0
#
# w_v = winds.values()
# for i, j in zip(winds.keys(), w_v):
#     print(i)
#     e = get_wind_energy_output(j)
#     print(e)
#     res += e
#
# print(res)

def get_wind_analysis():
    pass

