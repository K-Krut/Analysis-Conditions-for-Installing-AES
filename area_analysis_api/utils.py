import ee
from .ee_config import EE_CREDENTIALS

ee.Initialize(EE_CREDENTIALS)


# def get_ee_classification(coordinates):
#     polygon = ee.Geometry.Polygon([coordinates])
#
#     landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')
#     masked_landcover = landcover.clip(polygon)
#     info = landcover.clip(polygon).getInfo()
#     path = landcover.clip(polygon).getDownloadUrl()
#     print(landcover.getDownloadUrl({
#         'region': f'{coordinates}'
#     }))
#     print(path)
#     return info
#     # stats = masked_landcover.reduceRegion(reducer=ee.Reducer.frequencyHistogram(), geometry=polygon, scale=100)

def get_ee_classification(coordinates):
    coordinates = [
        [28.456259074773964, 50.32242765384289],
        [28.393602672186073, 50.305217330297616],
        [28.47256690558451, 50.30050258798011],
        [28.456259074773964, 50.32242765384289]
    ]
    # Create an Earth Engine polygon from the coordinates.
    polygon = ee.Geometry.Polygon(coordinates)

    # Select the 'discrete_classification' band from the COPERNICUS land cover image.
    landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')

    # Clip the image to the polygon and get download URL.
    path = landcover.getDownloadUrl({
        'scale': 3,  # Set the scale if necessary.
        'region': polygon.toGeoJSONString(),  # Convert the polygon to a GeoJSON string format.
        'format': 'png',
        "crs": "EPSG:3857",
        "crs_transform": [
            100,
            0,
            -20037550,
            0,
            -100,
            15538800
        ]
    })

    # Print the download URL to the console.
    print(path)
    print(polygon.area().getInfo())

    # Return the download URL.
    return landcover.clip(polygon).getInfo()
