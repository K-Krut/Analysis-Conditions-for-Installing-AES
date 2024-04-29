import joblib
import tensorflow as tf

model = tf.keras.models.load_model('landscape_model.keras')
scaler = joblib.load('scaler.gz')


# def prepare_polygon_data(polygon):
#     data = pd.DataFrame(polygon)
#     data = data.set_index('id')
#
#     predict_df = pd.DataFrame(index=data.index, columns=['area', 'percentage'])
#     predict_df['area'] = data['area']
#     predict_df['percentage'] = data['percentage']
#
#     scaled_data = scaler.transform(predict_df)
#     return scaled_data
#
#
# polygon_data = [
#     {"id": 40, "area": 0.38, "percentage": 65.54},
#     {"id": 114, "area": 0.17, "percentage": 29.21},
#     {"id": 125, "area": 0.03, "percentage": 5.17},
#     {"id": 115, "area": 0, "percentage": 0.42}
# ]
#
# prepared_data = prepare_polygon_data(polygon_data)
# prediction = model.predict(prepared_data)
# print("Prediction:", prediction)

