import uuid
import boto3
import numpy as np
from io import BytesIO
from matplotlib import pyplot as plt
from ai_models.weather_model.weather_utils import get_hourly_weather_data
from diploma_api.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME


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
    return df.groupby('month')  # return df.to_records()  # ['wdir', 'wspd', 'month', 'hour']


def draw_wind_rose(records, month):
    data = np.array(records, dtype=[('wdir', float), ('wspd', float), ('time', 'U5')])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.bar(np.radians(data['wdir']), data['wspd'], width=0.1, bottom=0.1)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    img_path = f"wind-roses/wind-rose-{month}-{uuid.uuid4()}.png"
    s3_client.put_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=img_path, Body=buf, ContentType='image/png')
    buf.close()
    plt.close(fig)
    return generate_presigned_url(img_path)


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
    yearly_data_weather = weather_for_wind_calculation(coords, [2022, 1], [2022, 12, 31])
    turbines_num = get_num_of_wind_turbines(area)
    monthly_data = []
    for month, data in yearly_data_weather:
        one_turbine_energy_out = round(sum(get_power(data['wspd'].to_numpy())))
        monthly_data.append(
            {
                "month": month,
                "wind_rose": draw_wind_rose_for_month_data(data, month),
                "energy": round(one_turbine_energy_out * turbines_num),  # kWh
                "energy_one_turbine": one_turbine_energy_out,  # kWh
                "max_wind_speed": round(data['wspd'].max()),  # м/c
                "average_wind_speed": round(data['wspd'].mean()),  # м/c
            }
        )

    return {
        "turbines": turbines_num,
        "wind_turbine_area": WIND_TURBINE_AREA,
        "wind_blade_length": WIND_BLADE_LEN,
        "month_energy_stats": monthly_data,
        "yearly_energy": sum([x.get("energy") for x in monthly_data]),
        "yearly_energy_one_turbine": sum([x.get("energy_one_turbine") for x in monthly_data])
    }


# coord = [35.2577876585286, 47.74093953469412]
#
# res = get_wind_energy_output(coord, 4)

m = {
    "turbines": 16,
    "wind_turbine_area": 0.25,
    "wind_blade_length": 50,
    "month_energy_stats": [
        {
            "month": 3,
            "wind_rose": "https://analysis-conditions-aes.s3.amazonaws.com/wind-roses/wind-rose-3-15fade97-2fd2-45f7-a1d9-ef6b9eb02941.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6KIEDAEC73CEXOYS%2F20240526%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240526T114046Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=325d362688841789948f0002ebe98e4981eb70c2a22b3c7ca6adf9aab43de5bb",
            "energy": 14940848,
            "energy_one_turbine": 933803,
            "max_wind_speed": 58,
            "average_wind_speed": 4
        },
        {
            "month": 4,
            "wind_rose": "https://analysis-conditions-aes.s3.amazonaws.com/wind-roses/wind-rose-4-f0f044ae-c836-4c18-a607-60af9b30be27.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6KIEDAEC73CEXOYS%2F20240526%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240526T114047Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e4e7fdef674f79dffae47b842104a6996e1ddc89f1a40a20291f8541f145520d",
            "energy": 4830816,
            "energy_one_turbine": 301926,
            "max_wind_speed": 43,
            "average_wind_speed": 4
        },
        {
            "month": 5,
            "wind_rose": "https://analysis-conditions-aes.s3.amazonaws.com/wind-roses/wind-rose-5-733cd16d-896b-48bf-a1a4-e03f0dcafff3.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6KIEDAEC73CEXOYS%2F20240526%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240526T114048Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cc58aec35976ad7975d03743d92cf14104607424e9582205c46811f079ea7c4e",
            "energy": 256,
            "energy_one_turbine": 16,
            "max_wind_speed": 2,
            "average_wind_speed": 2
        }
    ],
    "yearly_energy": 19771920,
    "yearly_energy_one_turbine": 1235745
}
