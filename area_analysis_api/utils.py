import ee

from .constants import landscape_types
from .ee_config import EE_CREDENTIALS

ee.Initialize(EE_CREDENTIALS)


def get_land_type_area_inside_polygon(polygon, class_mask):
    """
    Calculating area of the land type inside the difined polygon in km^2
    :param polygon:
    :param class_mask:
    :return:
    """
    class_area = class_mask.multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=polygon,
        scale=10).getInfo()
    return class_area['discrete_classification'] / 1e6


def get_polygon_area_m2(polygon):
    """
    Area of the polygon in square meters
    :param polygon: ee.Geometry.Polygon()
    :return: 113963.01695514935
    """
    return polygon.area().getInfo()


def get_polygon_area(polygon):
    """
    Area of the polygon in square km
    :param polygon: ee.Geometry.Polygon()
    :return: 113963.01695514935
    """
    return polygon.area().getInfo() / 1e6


def get_land_types_classification_results_sorted(results):
    """
    Sorting the results of the classification of landscape types within the polygon
    by their percentage of area to total polygon area
    :param results:
    :return:
    """
    return dict(sorted(results.items(), key=lambda item: item[1]['Percentage'], reverse=True))


def get_area_classification_details(landcover, polygon, polygon_area):
    results = {}

    for land_type in landscape_types:

        area = get_land_type_area_inside_polygon(polygon, landcover.eq(land_type))
        percentage = (area / polygon_area) * 100

        if percentage > 0:
            results[landscape_types[land_type]] = {
                'Area (sq km)': round(area, 2),
                'Percentage': round(percentage, 2)
            }

    # print(sum(value['Percentage'] for key, value in results.items() if value['Percentage'] > 0))
    return get_land_types_classification_results_sorted(results)


def get_ee_classification(coordinates):
    polygon = ee.Geometry.Polygon(coordinates)
    landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')

    polygon_area = get_polygon_area(polygon)

    land_types_stats = get_area_classification_details(landcover, polygon, polygon_area)

    return landcover.clip(polygon).getInfo(), land_types_stats
