import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

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
# model.fit(X_train_scaled, y_train, epochs=200, batch_size=1, verbose=1)

loss = model.evaluate(X_test_scaled, y_test)
print(f"Loss: {loss}")

model.save('landscape_model_v15.keras')
joblib.dump(scaler, 'landscape_scaler_v15.gz')


def prepare_and_predict(data):
    features = {}

    for col in X_train.columns:
        features[col] = 0

    for item in data:
        features[f'area_id_{item["id"]}'] = item['area']
        features[f'perc_id_{item["id"]}'] = item['percentage']

    return pd.DataFrame([features])


# test_data = prepare_and_predict()
# test_data_scaled = scaler.transform(test_data)
# prediction = model.predict(test_data_scaled)
# print(f"Prediction: {prediction[0][0]}")
#

def test_model():
    data_for_test = [
        [
            [{'area': 0.13197791578506768, 'percentage': 100.33747335079923, 'id': 40}],
            1
        ],
        [
            [
                {'id': 40, 'area': 1.61, 'percentage': 47.64},
                {'id': 114, 'area': 1.44, 'percentage': 42.58},
                {'id': 115, 'area': 0.19, 'percentage': 5.76},
                {'id': 126, 'area': 0.1, 'percentage': 2.88},
                {'id': 124, 'area': 0.02, 'percentage': 0.64},
                {'id': 125, 'area': 0.02, 'percentage': 0.48},
                {'id': 116, 'area': 0.01, 'percentage': 0.36}
            ],
            -1
        ],
        [
            [
                {'area': 0.33, 'percentage': 70.92, 'id': 114},
                {'area': 0.09, 'percentage': 18.45, 'id': 40},
                {'area': 0.04, 'percentage': 8.7, 'id': 124},
                {'area': 0.01, 'percentage': 1.17, 'id': 125},
                {'area': 0.01, 'percentage': 1.11, 'id': 126}
            ],
            -1
        ],
        [
            [
                {'area': 1.22, 'percentage': 52.5, 'id': 40},
                {'area': 1.04, 'percentage': 44.53, 'id': 114},
                {'area': 0.03, 'percentage': 1.4, 'id': 126},
                {'area': 0.03, 'percentage': 1.22, 'id': 124},
                {'area': 0.01, 'percentage': 0.35, 'id': 115},
                {'area': 0.01, 'percentage': 0.35, 'id': 125}
            ],
            -1
        ],
        [
            [
                {'area': 0.24, 'percentage': 88.23, 'id': 80},
                {'area': 0.03, 'percentage': 12.1, 'id': 90},
                {'area': 0.0, 'percentage': 0.01, 'id': 126}
            ],
            0
        ],
        [
            [
                {'area': 0.32, 'percentage': 73.1, 'id': 50},
                {'area': 0.09, 'percentage': 19.69, 'id': 40},
                {'area': 0.03, 'percentage': 7.56, 'id': 126}
            ],
            0
        ],
        [
            [{'area': 2.310349462552525, 'percentage': 100.32721539149713, 'id': 80}],
            0
        ],
        [
            [{'area': 0.085, 'percentage': 53.5, 'id': 40}, {'area': 0.030, 'percentage': 19.1, 'id': 115},
             {'area': 0.022, 'percentage': 14.2, 'id': 111}, {'area': 0.022, 'percentage': 13.8, 'id': 126}],
            -1
        ],
        [
            [{'area': 8.5, 'percentage': 93.4, 'id': 40}, {'area': 0.59, 'percentage': 6.4, 'id': 30},
             {'area': 0.03, 'percentage': 0.3, 'id': 126}],
            1
        ],
        [
            [{'area': 0.5076616215332478, 'percentage': 37.668938530957114, 'id': 40},
             {'area': 0.44197429261543425, 'percentage': 32.794880988859006, 'id': 30},
             {'area': 0.3453316021359459, 'percentage': 25.6239084104252, 'id': 114},
             {'area': 0.033078659707222735,  'percentage': 2.4544656250250254, 'id': 126},
             {'area': 0.01860648452758789, 'percentage': 1.3806175062634911, 'id': 125},
             {'area': 0.004651780128479004, 'percentage': 0.34516617425201085, 'id': 115}],
            -1
        ],
        [
            [{'area': 5.872277599406364, 'percentage': 64.24947454606017, 'id': 40}, {'area': 1.9977788383586357, 'percentage': 21.85799946459556, 'id': 114}, {'area': 0.7490939792231547, 'percentage': 8.195950163454537, 'id': 124}, {'area': 0.38933821854895795, 'percentage': 4.259808147523281, 'id': 115}, {'area': 0.08969279174643123, 'percentage': 0.9813423569859792, 'id': 126}, {'area': 0.0707248062560736, 'percentage': 0.7738107680372602, 'id': 125}],
            -1
        ],
        [
            [{'area': 0.7422016827392578, 'percentage': 97.66462290047555, 'id': 114}, {'area': 0.016309992752075196, 'percentage': 2.146194664719612, 'id': 125}, {'area': 0.004077351303100586, 'percentage': 0.5365293379292663, 'id': 115}],
            0
        ],

    ]
    for i in data_for_test:
        test_data = prepare_and_predict(i[0])
        test_data_scaled = scaler.transform(test_data)
        print(f"    Prediction: {round(model.predict(test_data_scaled)[0][0], 2)} --- {i[1]} Expected")


test_model()
