import ee
from ee_config import EE_CREDENTIALS

# ee.Initialize()
ee.Initialize(EE_CREDENTIALS)


def get_ee_classification(coordinates):
    polygon = ee.Geometry.Polygon([coordinates])

    landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019")
    # landcover1 = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')
    masked_landcover = landcover.clip(polygon)
    print(landcover.clip(polygon).getInfo())
    # stats = masked_landcover.reduceRegion(
    #     reducer=ee.Reducer.frequencyHistogram(),
    #     geometry=polygon,
    #     scale=100
    # )
    #
    # print(stats.getInfo())


data = [
    [50.979462961275296, 32.04050867152585],
    [50.95002917143124, 32.009151416460035],
    [50.946231221870775, 32.08974956567584]
]


get_ee_classification(data)
