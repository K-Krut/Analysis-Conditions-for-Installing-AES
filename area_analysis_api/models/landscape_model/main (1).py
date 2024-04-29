import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from data_for_train import polygons, outcomes

all_data = []

for polygon, outcome in zip(polygons, outcomes):
    poly_dict = {'outcome': outcome}
    for land_type in polygon:
        poly_dict[f'area_id_{land_type["id"]}'] = land_type['area']
        poly_dict[f'perc_id_{land_type["id"]}'] = land_type['percentage']
    all_data.append(poly_dict)

df = pd.DataFrame(all_data)
df.fillna(0, inplace=True)

X = df.drop('outcome', axis=1)
y = df['outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential([
    Dense(10, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(10, activation='relu'),
    Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train_scaled, y_train, epochs=200, batch_size=1, verbose=1)

loss = model.evaluate(X_test_scaled, y_test)
print(f"Loss: {loss}")


def prepare_and_predict(data):
    features = {}

    for col in X_train.columns:
        features[col] = 0

    for item in data:
        features[f'area_id_{item["id"]}'] = item['area']
        features[f'perc_id_{item["id"]}'] = item['percentage']

    return pd.DataFrame([features])


api_data = [
    {
        "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest and a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate forest or shrub land cover type.\n",
        "area": 0.37,
        "percentage": 62.91,
        "id": 40
    },
    {
        "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf tree communities with an annual cycle of leaf-on and leaf-off periods.\n",
        "area": 0.2,
        "percentage": 33.94,
        "id": 114
    },
    {
        "name": "Open forest, mixed.",
        "area": 0.02,
        "percentage": 2.79,
        "id": 125
    },
    {
        "name": "Closed forest, mixed.",
        "area": 0,
        "percentage": 0.7,
        "id": 115
    }
]


test_data = prepare_and_predict(api_data)
test_data_scaled = scaler.transform(test_data)
prediction = model.predict(test_data_scaled)
print(f"Prediction: {prediction}")





# Сохранение обученной модели
# model.save('my_model.h5')
model.save('landscape_model_1')
# Сохранение масштабировщика
import joblib
joblib.dump(scaler, 'scaler.gz')
