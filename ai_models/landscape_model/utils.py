import joblib
import tensorflow as tf
import pandas as pd

# scaler = joblib.load('../../landscape_scaler_3.gz')
# model = tf.keras.models.load_model('../../landscape_model_3.keras')
# print(model.input_shape)
# print(scaler.feature_names_in_)


# FEATURES_COLS = ['area_id_0', 'perc_id_0', 'area_id_20', 'perc_id_20', 'area_id_30', 'perc_id_30', 'area_id_40',
#                  'perc_id_40', 'area_id_50', 'perc_id_50', 'area_id_60', 'perc_id_60',
#                  'area_id_70', 'perc_id_70', 'area_id_80', 'perc_id_80', 'area_id_90', 'perc_id_90', 'area_id_100',
#                  'perc_id_100', 'area_id_111', 'perc_id_111', 'area_id_112', 'perc_id_112', 'area_id_113',
#                  'perc_id_113', 'area_id_114', 'perc_id_114', 'area_id_115', 'perc_id_115', 'area_id_116',
#                  'perc_id_116', 'area_id_121', 'perc_id_121', 'area_id_122', 'perc_id_122', 'area_id_123',
#                  'perc_id_123', 'area_id_124', 'perc_id_124', 'area_id_125', 'perc_id_125', 'area_id_126',
#                  'perc_id_126', 'area_id_200', 'perc_id_200']

FEATURES_COLS = [
    'area_id_40', 'perc_id_40', 'area_id_114', 'perc_id_114', 'area_id_115',
    'perc_id_115', 'area_id_126', 'perc_id_126', 'area_id_124', 'perc_id_124',
    'area_id_125', 'perc_id_125', 'area_id_116', 'perc_id_116', 'area_id_50',
    'perc_id_50', 'area_id_90', 'perc_id_90', 'area_id_80', 'perc_id_80',
    'area_id_30', 'perc_id_30', 'area_id_111', 'perc_id_111', 'area_id_121',
    'perc_id_121', 'area_id_20', 'perc_id_20', 'area_id_100', 'perc_id_100',
    'area_id_60', 'perc_id_60', 'area_id_122', 'perc_id_122', 'area_id_123',
    'perc_id_123', 'area_id_112', 'perc_id_112', 'area_id_113', 'perc_id_113',
    'area_id_70', 'perc_id_70', 'area_id_200', 'perc_id_200', 'area_id_0',
    'perc_id_0'
]


def convert_polygon_stats(polygon_data):
    print('convert_polygon_stats')
    polygon_data_features = {}

    for i in polygon_data:
        polygon_data_features[f'area_id_{i["id"]}'] = i["area"]
        polygon_data_features[f'perc_id_{i["id"]}'] = i["percentage"]

    return polygon_data_features


def predict_polygon(data, model, scaler):
    features = {feature_id: 0 for feature_id in FEATURES_COLS}

    for key, value in data.items():
        if key in features:
            features[key] = value

    df = pd.DataFrame([features])

    X_scaled = scaler.transform(df)

    return model.predict(X_scaled)[0][0]
