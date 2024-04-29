import joblib
import pandas as pd
import tensorflow as tf

scaler = joblib.load('scaler.gz')
model = tf.keras.models.load_model('landscape_model.keras')

FEATURES_COLS = ['area_id_40', 'perc_id_40', 'area_id_114', 'perc_id_114', 'area_id_115',
                 'perc_id_115', 'area_id_126', 'perc_id_126', 'area_id_124',
                 'perc_id_124', 'area_id_125', 'perc_id_125', 'area_id_116',
                 'perc_id_116', 'area_id_50', 'perc_id_50', 'area_id_90', 'perc_id_90',
                 'area_id_80', 'perc_id_80', 'area_id_30', 'perc_id_30']


def convert_polygon_stats(polygon_data):
    polygon_data_features = {}

    for i in polygon_data:
        polygon_data_features[f'area_id_{i["id"]}'] = i["area"]
        polygon_data_features[f'perc_id_{i["id"]}'] = i["percentage"]

    return polygon_data_features


def predict_polygon(data):
    features = {feature_id: 0 for feature_id in FEATURES_COLS}

    for key, value in data.items():
        if key in features:
            features[key] = value

    df = pd.DataFrame([features])

    X_scaled = scaler.transform(df)

    return model.predict(X_scaled)


# polygon = [
#     {
#         "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
#         "area": 0.01,
#         "percentage": 77.33,
#         "id": 40
#     },
#     {
#         "name": "Open forest, not matching any of the other definitions.",
#         "area": 0.0,
#         "percentage": 22.97,
#         "id": 126
#     }
# ]
#
# polygon_converted = convert_polygon_stats(polygon)
#
# print(predict_polygon(polygon_converted))
