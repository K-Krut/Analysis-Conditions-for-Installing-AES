import joblib
import pandas as pd
import tensorflow as tf

# model = tf.keras.models.load_model('landscape_model.keras')
scaler = joblib.load('scaler.gz')
model = tf.keras.layers.TFSMLayer("landscape_model_files", call_endpoint="serving_default")


# def prepare_polygon_data(polygon):
#     # Подготовка DataFrame с правильными названиями столбцов
#     features = {f'area_id_{item["id"]}': [item['area']] for item in polygon}
#     features.update({f'perc_id_{item["id"]}': [item['percentage']] for item in polygon})
#     ids = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 111, 112, 113, 114, 115, 116, 121, 122, 123, 124, 125, 126, 200]
#
#     required_columns = []
#     for id_ in ids:
#         required_columns.append(f'area_id_{id_}')
#         required_columns.append(f'perc_id_{id_}')
#
#     print(required_columns)
#     for column in required_columns:
#         if column not in features:
#             features[column] = [0]  # Добавляем недостающие столбцы со значением 0
#
#     # Создание DataFrame
#     df = pd.DataFrame(features)
#
#     # Применение масштабировщика
#     scaled_data = scaler.transform(df)
#     return scaled_data
#
#
# # Пример данных полигона
# polygon_data = [
#     {"id": 40, "area": 0.38, "percentage": 65.54},
#     {"id": 114, "area": 0.17, "percentage": 29.21},
#     {"id": 125, "area": 0.03, "percentage": 5.17},
#     {"id": 115, "area": 0, "percentage": 0.42}
# ]
#
# # Подготовка и прогноз
# prepared_data = prepare_polygon_data(polygon_data)
# prediction = model.predict(prepared_data)
# print("Prediction:", prediction)




def prepare_polygon_data(polygon):
    ids = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 111, 112, 113, 114, 115, 116, 121, 122, 123, 124, 125, 126, 200]

    feature_dict = {'area_id_0': 0, 'area_id_20': 0, 'area_id_30': 0, 'area_id_40': 0, 'area_id_50': 0, 'area_id_60': 0,
                    'area_id_70': 0, 'area_id_80': 0, 'area_id_90': 0, 'area_id_100': 0, 'area_id_111': 0,
                    'area_id_112': 0, 'area_id_113': 0, 'area_id_114': 0, 'area_id_115': 0, 'area_id_116': 0,
                    'area_id_121': 0, 'area_id_122': 0, 'area_id_123': 0, 'area_id_124': 0, 'area_id_125': 0,
                    'area_id_126': 0, 'area_id_200': 0, 'perc_id_0': 0, 'perc_id_20': 0, 'perc_id_30': 0,
                    'perc_id_40': 0, 'perc_id_50': 0, 'perc_id_60': 0, 'perc_id_70': 0, 'perc_id_80': 0,
                    'perc_id_90': 0, 'perc_id_100': 0, 'perc_id_111': 0, 'perc_id_112': 0, 'perc_id_113': 0,
                    'perc_id_114': 0, 'perc_id_115': 0, 'perc_id_116': 0, 'perc_id_121': 0, 'perc_id_122': 0,
                    'perc_id_123': 0, 'perc_id_124': 0, 'perc_id_125': 0, 'perc_id_126': 0, 'perc_id_200': 0}

    for item in polygon:
        feature_dict[f'area_id_{item["id"]}'] = item['area']
        feature_dict[f'perc_id_{item["id"]}'] = item['percentage']

    print(feature_dict)
    print(feature_dict['area_id_113'])

    df = pd.DataFrame([feature_dict])

    scaled_data = scaler.transform(df)
    return scaled_data


polygon_data = [
    {"id": 40, "area": 0.38, "percentage": 65.54},
    {"id": 114, "area": 0.17, "percentage": 29.21},
    {"id": 125, "area": 0.03, "percentage": 5.17},
    {"id": 115, "area": 0, "percentage": 0.42}
]

prepared_data = prepare_polygon_data(polygon_data)
prediction = model.predict(prepared_data)
print("Prediction:", prediction)

import joblib
import tensorflow as tf
import pandas as pd

model = tf.keras.models.load_model('landscape_model.keras')
scaler = joblib.load('scaler.gz')


def predict_polygon(data):
    all_ids = ['area_id_40', 'perc_id_40', 'area_id_114', 'perc_id_114', 'area_id_115',
               'perc_id_115', 'area_id_126', 'perc_id_126', 'area_id_124',
               'perc_id_124', 'area_id_125', 'perc_id_125', 'area_id_116',
               'perc_id_116', 'area_id_50', 'perc_id_50', 'area_id_90', 'perc_id_90',
               'area_id_80', 'perc_id_80', 'area_id_30', 'perc_id_30']

    features = {feature_id: 0 for feature_id in all_ids}

    for key, value in data.items():
        if key in features:
            features[key] = value

    df = pd.DataFrame([features])

    X_scaled = scaler.transform(df)

    return model.predict(X_scaled)


polygon_data = {
    'perc_id_40': 65.54,
    'area_id_40': 0.38,
    'area_id_114': 0.17,
    'area_id_125': 0.03,
    'area_id_115': 0.00,
    'perc_id_114': 29.21,
    'perc_id_125': 5.17,
    'perc_id_115': 0.42
}

result = predict_polygon(polygon_data)
print("Prediction Result:", result)

polygon = [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.01,
            "percentage": 77.33,
            "id": 40
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 22.97,
            "id": 126
        }
    ]

polygon_data_features = {}

for i in polygon:
    polygon_data_features[f'area_id_{i["id"]}'] = i["area"]
    polygon_data_features[f'perc_id_{i["id"]}'] = i["percentage"]


print(polygon_data_features)