import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

polygons = [
    [
        {"id": 40, "area": 1.93, "percentage": 47.57},
        {"id": 114, "area": 1.73, "percentage": 42.73},
        {"id": 115, "area": 0.20, "percentage": 4.82},
        {"id": 126, "area": 0.12, "percentage": 2.91},
        {"id": 124, "area": 0.07, "percentage": 1.61},
        {"id": 125, "area": 0.02, "percentage": 0.40},
        {"id": 116, "area": 0.01, "percentage": 0.30}
    ],
    [
        {"id": 40, "area": 0.27, "percentage": 100.34}
    ],
    [
        {"id": 114, "area": 1.02, "percentage": 98.77},
        {"id": 124, "area": 0.02, "percentage": 1.58}
    ],
    [
        {"id": 40, "area": 0.38, "percentage": 65.54},
        {"id": 114, "area": 0.17, "percentage": 29.21},
        {"id": 125, "area": 0.03, "percentage": 5.17},
        {"id": 115, "area": 0.00, "percentage": 0.42}
    ],
    [
        {"id": 50, "area": 0.09, "percentage": 100.34}
    ],
    [
        {"id": 40, "area": 1.93, "percentage": 47.57},
        {"id": 114, "area": 1.73, "percentage": 42.73},
        {"id": 115, "area": 0.20, "percentage": 4.82},
        {"id": 126, "area": 0.12, "percentage": 2.91},
        {"id": 124, "area": 0.07, "percentage": 1.61},
        {"id": 125, "area": 0.02, "percentage": 0.40},
        {"id": 116, "area": 0.01, "percentage": 0.30}
    ],
    [
        {"id": 40, "area": 0.27, "percentage": 100.34}
    ],
    [
        {"id": 114, "area": 1.02, "percentage": 98.77},
        {"id": 124, "area": 0.02, "percentage": 1.58}
    ],
    [
        {"id": 40, "area": 0.38, "percentage": 65.54},
        {"id": 114, "area": 0.17, "percentage": 29.21},
        {"id": 125, "area": 0.03, "percentage": 5.17},
        {"id": 115, "area": 0.00, "percentage": 0.42}
    ],
    [
        {"id": 50, "area": 0.09, "percentage": 100.34}
    ],
    [
        {'id': 40, 'area': 0.53, 'percentage': 80.81}, {'id': 114, 'area': 0.1, 'percentage': 16.1},
        {'id': 115, 'area': 0.02, 'percentage': 3.12}, {'id': 126, 'area': 0.0, 'percentage': 0.31}
    ],
    [
        {'id': 126, 'area': 0.12, 'percentage': 31.44}, {'id': 125, 'area': 0.11, 'percentage': 30.12},
        {'id': 90, 'area': 0.08, 'percentage': 20.35}, {'id': 50, 'area': 0.04, 'percentage': 9.63},
        {'id': 40, 'area': 0.02, 'percentage': 5.55}, {'id': 80, 'area': 0.01, 'percentage': 3.26}
    ],
    [
        {'id': 126, 'area': 0.28, 'percentage': 29.14}, {'id': 40, 'area': 0.25, 'percentage': 25.75},
        {'id': 125, 'area': 0.12, 'percentage': 12.1}, {'id': 50, 'area': 0.09, 'percentage': 8.91},
        {'id': 80, 'area': 0.08, 'percentage': 8.85}, {'id': 90, 'area': 0.07, 'percentage': 6.91},
        {'id': 30, 'area': 0.06, 'percentage': 6.49}, {'id': 124, 'area': 0.02, 'percentage': 1.77},
        {'id': 115, 'area': 0, 'percentage': 0.42}, {'id': 114, 'area': 0, 'percentage': 0.01}
    ],
    [
        {'id': 40, 'area': 0.71, 'percentage': 100.35}
    ],
    [
        {'id': 114, 'area': 0.36, 'percentage': 47.39}, {'id': 40, 'area': 0.32, 'percentage': 42.22},
        {'id': 126, 'area': 0.04, 'percentage': 4.82}, {'id': 116, 'area': 0.02, 'percentage': 2.15},
        {'id': 115, 'area': 0.02, 'percentage': 2.14}, {'id': 125, 'area': 0.01, 'percentage': 1.62}
    ],
    [
        {'id': 40, 'area': 0.38, 'percentage': 100.35}
    ],
    [
        {'id': 114, 'area': 0.36, 'percentage': 51.68}, {'id': 40, 'area': 0.31, 'percentage': 44.04},
        {'id': 115, 'area': 0.01, 'percentage': 1.73}, {'id': 126, 'area': 0.01, 'percentage': 1.73},
        {'id': 124, 'area': 0.01, 'percentage': 1.16}
    ],
    [
        {'id': 80, 'area': 0.05, 'percentage': 85.69}, {'id': 126, 'area': 0, 'percentage': 7.74},
        {'id': 90, 'area': 0, 'percentage': 5.2}, {'id': 30, 'area': 0, 'percentage': 1.24},
        {'id': 40, 'area': 0, 'percentage': 0.46}],
    [
        {'id': 40, 'area': 0.14, 'percentage': 100.35}
    ],
    [
        {'id': 114, 'area': 0.78, 'percentage': 59.25}, {'id': 40, 'area': 0.49, 'percentage': 36.97},
        {'id': 126, 'area': 0.02, 'percentage': 1.38}, {'id': 115, 'area': 0.02, 'percentage': 1.23},
        {'id': 125, 'area': 0.02, 'percentage': 1.22}, {'id': 116, 'area': 0.0, 'percentage': 0.31}],
    [
        {'id': 50, 'area': 2.71, 'percentage': 98.24}, {'id': 126, 'area': 0.05, 'percentage': 1.77},
        {'id': 40, 'area': 0.01, 'percentage': 0.34}
    ],
    [
        {'id': 40, 'area': 0.97, 'percentage': 86.96}, {'id': 50, 'area': 0.15, 'percentage': 13.39}
    ],
    [
        {'id': 40, 'area': 0.39, 'percentage': 64.2}, {'id': 50, 'area': 0.22, 'percentage': 36.15},
        {'id': 126, 'area': 0, 'percentage': 0}
    ],
    [
        {'id': 40, 'area': 1.25, 'percentage': 58.64}, {'id': 114, 'area': 0.74, 'percentage': 35.05},
        {'id': 126, 'area': 0.06, 'percentage': 2.63}, {'id': 115, 'area': 0.04, 'percentage': 2.11},
        {'id': 125, 'area': 0.02, 'percentage': 1.15}, {'id': 124, 'area': 0.02, 'percentage': 0.77}
    ],
    [
        {'id': 40, 'area': 0.71, 'percentage': 54.65}, {'id': 114, 'area': 0.53, 'percentage': 41.26},
        {'id': 126, 'area': 0.04, 'percentage': 2.77}, {'id': 124, 'area': 0.02, 'percentage': 1.26},
        {'id': 125, 'area': 0.01, 'percentage': 0.41}
    ],
    [
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.05,
            "percentage": 97.05,
            "id": 126
        },
        {
            "name": "Closed forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 3.28,
            "id": 116
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.22,
            "percentage": 100.32,
            "id": 40
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 0.02,
            "id": 126
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.37,
            "percentage": 86.54,
            "id": 40
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.06,
            "percentage": 13.8,
            "id": 126
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.0,
            "percentage": 0.01,
            "id": 30
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.6,
            "percentage": 99.82,
            "id": 40
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.0,
            "percentage": 0.53,
            "id": 30
        }
    ],
    [
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 2.23,
            "percentage": 92.93,
            "id": 114
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.07,
            "percentage": 2.75,
            "id": 115
        },
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.06,
            "percentage": 2.6,
            "id": 40
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.03,
            "percentage": 1.36,
            "id": 125
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.02,
            "percentage": 0.71,
            "id": 126
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.17,
            "percentage": 38.77,
            "id": 40
        },
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.15,
            "percentage": 33.5,
            "id": 114
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.07,
            "percentage": 17.06,
            "id": 126
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.03,
            "percentage": 6.49,
            "id": 125
        },
        {
            "name": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.01,
            "percentage": 2.47,
            "id": 124
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.01,
            "percentage": 1.85,
            "id": 115
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.0,
            "percentage": 0.2,
            "id": 30
        }
    ],
    [
        {
            "name": "Urban / built up. Land covered by buildings and other man-made structures.",
            "area": 1.07,
            "percentage": 38.91,
            "id": 50
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.55,
            "percentage": 20.1,
            "id": 126
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.44,
            "percentage": 15.98,
            "id": 30
        },
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.2,
            "percentage": 7.38,
            "id": 40
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.18,
            "percentage": 6.44,
            "id": 125
        },
        {
            "name": "Herbaceous wetland. Lands with a permanent mixture of water and herbaceous\nor woody vegetation. The vegetation can be present in either salt,\nbrackish, or fresh water.\n",
            "area": 0.18,
            "percentage": 6.43,
            "id": 90
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.08,
            "percentage": 2.77,
            "id": 115
        },
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.04,
            "percentage": 1.6,
            "id": 114
        },
        {
            "name": "Closed forest, not matching any of the other definitions.",
            "area": 0.02,
            "percentage": 0.58,
            "id": 116
        },
        {
            "name": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.0,
            "percentage": 0.15,
            "id": 124
        },
        {
            "name": "Permanent water bodies. Lakes, reservoirs, and rivers. Can be either fresh or salt-water bodies.",
            "area": 0.0,
            "percentage": 0.01,
            "id": 80
        }
    ],
    [
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 1.02,
            "percentage": 52.85,
            "id": 114
        },
        {
            "name": "Urban / built up. Land covered by buildings and other man-made structures.",
            "area": 0.5,
            "percentage": 26.23,
            "id": 50
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.34,
            "percentage": 17.62,
            "id": 115
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.05,
            "percentage": 2.73,
            "id": 125
        },
        {
            "name": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.02,
            "percentage": 0.78,
            "id": 124
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 0.1,
            "id": 126
        },
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.0,
            "percentage": 0.03,
            "id": 40
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 1.85,
            "percentage": 85.41,
            "id": 40
        },
        {
            "name": "Urban / built up. Land covered by buildings and other man-made structures.",
            "area": 0.23,
            "percentage": 10.81,
            "id": 50
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.05,
            "percentage": 2.22,
            "id": 30
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.04,
            "percentage": 1.71,
            "id": 126
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.0,
            "percentage": 0.21,
            "id": 115
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.0,
            "percentage": 0.0,
            "id": 125
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 1.25,
            "percentage": 100.35,
            "id": 40
        },
        {
            "name": "Urban / built up. Land covered by buildings and other man-made structures.",
            "area": 0.0,
            "percentage": 0.0,
            "id": 50
        }
    ],
    [
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 2.47,
            "percentage": 51.71,
            "id": 114
        },
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 2.07,
            "percentage": 43.34,
            "id": 40
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.07,
            "percentage": 1.53,
            "id": 125
        },
        {
            "name": "Closed forest, mixed.",
            "area": 0.06,
            "percentage": 1.22,
            "id": 115
        },
        {
            "name": "Herbaceous vegetation. Plants without persistent stem or shoots above ground\nand lacking definite firm structure. Tree and shrub cover is less\nthan 10 %.\n",
            "area": 0.04,
            "percentage": 0.83,
            "id": 30
        },
        {
            "name": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.04,
            "percentage": 0.74,
            "id": 124
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.03,
            "percentage": 0.64,
            "id": 126
        },
        {
            "name": "Closed forest, not matching any of the other definitions.",
            "area": 0.02,
            "percentage": 0.34,
            "id": 116
        }
    ],
    [
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 6.91,
            "percentage": 100.35,
            "id": 40
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 0.0,
            "id": 126
        }
    ],
    [
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
    ],
    [
        {
            "name": "Urban / built up. Land covered by buildings and other man-made structures.",
            "area": 0.03,
            "percentage": 49.16,
            "id": 50
        },
        {
            "name": "Open forest, mixed.",
            "area": 0.01,
            "percentage": 25.62,
            "id": 125
        },
        {
            "name": "Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest\nand a bare soil period (e.g., single and multiple cropping systems).\nNote that perennial woody crops will be classified as the appropriate\nforest or shrub land cover type.\n",
            "area": 0.01,
            "percentage": 13.79,
            "id": 40
        },
        {
            "name": "Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs\nand grassland, consists of seasonal broadleaf tree communities with\nan annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.0,
            "percentage": 7.85,
            "id": 124
        },
        {
            "name": "Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf\ntree communities with an annual cycle of leaf-on and leaf-off periods.\n",
            "area": 0.0,
            "percentage": 3.02,
            "id": 114
        },
        {
            "name": "Open forest, not matching any of the other definitions.",
            "area": 0.0,
            "percentage": 0.9,
            "id": 126
        }
    ]
]

outcomes = [-1, 1, 0, -1, 0, -1, 1, 0, -1, 0, -1, 0, 0, 1, -1, 1, -1, -1, 1, -1, 0, -1, -1, -1, -1, 0, 1, -1, 1, 0, -1,
            0, 0, -1, 1, -1, 1, -1, 0]

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
