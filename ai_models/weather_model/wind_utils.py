import uuid
import boto3
import base64
import ≈ as np
from io import BytesIO
from ai_models.weather_model.weather_utils import get_hourly_weather_data
from diploma_api.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME

import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt


WIND_TURBINE_AREA = 0.25  # км², для турбины с лопастями 50м, 5 размахов
WIND_BLADE_LEN = 50  # Vestas V112-3.45 MW - 54,6 m

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)


def generate_presigned_url(object_key, expiration=3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': object_key},
        ExpiresIn=expiration
    )


def weather_for_wind_calculation(coords, ds, de):
    df = get_hourly_weather_data(coords, ds, de)
    df = df.drop(columns=['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'pres', 'tsun', 'coco', 'wpgt'])
    df['month'] = df.index.month
    df['hour'] = [str(x[0])[11:16] for x in df.to_records()]
    df['wdir'] = df['wdir'].fillna(0)
    df['wspd'] = df['wspd'].fillna(0)
    df['wspd'] = df['wspd'] / 3.6
    return df  # return df.to_records()  # ['wdir', 'wspd', 'month', 'hour']


def draw_wind_rose(records, month):
    data = np.array(records, dtype=[('wdir', float), ('wspd', float), ('time', 'U5')])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.bar(np.radians(data['wdir']), data['wspd'], width=0.1, bottom=0.1)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    img_path = f"wind-roses/wind-rose-{month}-{uuid.uuid4()}.png"
    s3_client.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=img_path, Body=buf, ContentType='image/png')

    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('utf-8')

    buf.close()
    plt.close(fig)
    return generate_presigned_url(img_path), base64_image


def draw_wind_rose_for_month_data(data, month):
    group = data.drop(columns=['month'])
    try:
        return draw_wind_rose(group.to_records(index=False), month)
    except Exception as e:
        print(e, group.to_records(index=False))
        return None


def get_wind_rose_for_year(yearly_weather_data):
    for name, group in yearly_weather_data:
        group = group.drop(columns=['month'])
        draw_wind_rose(group.to_records(index=False), name)


def get_wind_speeds(yearly_weather_data):
    speeds = {}
    for month, group in yearly_weather_data:
        speeds[month] = group['wspd'].to_numpy()
    return speeds


def get_power(wind_speeds, r=WIND_BLADE_LEN):
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
    return (0.5 * rho * A * ((wind_speeds) ** 3) * Cp * 0.9) / 1000


def get_num_of_wind_turbines(area):
    return round(area / WIND_TURBINE_AREA)


def get_wind_energy_output(coords, area):
    print("get_wind_energy_output")
    yearly_data_weather = weather_for_wind_calculation(coords, [2022, 1], [2022, 12, 31])
    yearly_data_weather_grouped = yearly_data_weather.groupby('month')
    turbines_num = get_num_of_wind_turbines(area)
    yearly_wind_rose = draw_wind_rose_for_month_data(yearly_data_weather, "yearly_wind_rose")
    monthly_data = []
    for month, data in yearly_data_weather_grouped:
        one_turbine_energy_out = round(sum(get_power(data['wspd'].to_numpy())))
        wind_rose_img = draw_wind_rose_for_month_data(data, month)
        monthly_data.append(
            {
                "month": month,
                "wind_rose": wind_rose_img[0],
                "wind_rose_base_64": wind_rose_img[1],
                "energy": round(one_turbine_energy_out * turbines_num),  # kWh
                "energy_one_turbine": round(one_turbine_energy_out),  # kWh
                "max_wind_speed": round(data['wspd'].max()),  # м/c
                "average_wind_speed": round(data['wspd'].mean()),  # м/c
            }
        )
    return {
        "turbines": turbines_num,
        "wind_turbine_area": WIND_TURBINE_AREA,
        "wind_blade_length": WIND_BLADE_LEN,
        "month_energy_stats": monthly_data,
        "yearly_energy_one_turbine": sum([x.get("energy_one_turbine") for x in monthly_data]),
        "yearly_wind_rose": {
            "url": yearly_wind_rose[0],
            "base_64_data": yearly_wind_rose[1]
        },
        "max_wind_speed": round(yearly_data_weather['wspd'].max()),  # м/c
        "average_wind_speed": round(yearly_data_weather['wspd'].mean()),  # м/c
        "average_wind_angle": round(yearly_data_weather['wdir'].mean()),  # в градусах
        "yearly_energy": sum([x.get("energy") for x in monthly_data]),
    }
