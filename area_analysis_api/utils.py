import ee
import joblib

import keras
from ai_models.landscape_model.utils import predict_polygon, convert_polygon_stats
from ai_models.weather_model.weather_utils import get_energy_output_stats
from .constants import landscape_types, FILTERING_AREAS_SCALE, landscape_types_details, MIN_POLYGON_AREA, SUITABLE_TYPES
from .ee_config import EE_CREDENTIALS

scaler = joblib.load('landscape_scaler_v20.gz')
model = keras.models.load_model('landscape_model_v20.keras')
ee.Initialize(EE_CREDENTIALS)
landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')


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
    return sorted(results, key=lambda x: x['percentage'], reverse=True)


def get_area_classification_details(landcover, polygon, polygon_area):
    results = []

    for land_type in landscape_types:

        area = get_land_type_area_inside_polygon(polygon, landcover.eq(land_type))
        percentage = (area / polygon_area) * 100

        if percentage > 0:
            results.append(
                {
                    'name': landscape_types[land_type],
                    'area': area,
                    'percentage': percentage,
                    'id': land_type
                }
            )
    return get_land_types_classification_results_sorted(results)


def get_connected_area(masked_landcover):
    """
    Function for filtering areas
    :param masked_landcover:
    :return:
    """
    class_mask_40 = masked_landcover.eq(40)
    class_mask_60 = masked_landcover.eq(60)
    class_mask_100 = masked_landcover.eq(100)
    class_mask_30 = masked_landcover.eq(30)
    combined_mask = class_mask_40.Or(class_mask_60).Or(class_mask_30).Or(class_mask_100)
    connected = combined_mask.connectedComponents(connectedness=ee.Kernel.plus(1), maxSize=1024)
    return connected.select('labels').connectedPixelCount(maxSize=1024)


def get_largest_area_mask(connected_areas, polygon):
    """
    Get mask of filtered area
    :param connected_areas:
    :param polygon:
    :return:
    """
    largest_area_label = connected_areas.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=polygon,
        scale=FILTERING_AREAS_SCALE,
        maxPixels=1e13
    ).get('labels')

    return connected_areas.updateMask(connected_areas.eq(ee.Number(largest_area_label)))


def get_filtered_area_coordinates(polygon, landcover):
    """
    Function for defining filtered area coordinates
    :param polygon:
    :param landcover:
    :return:
    """
    masked_landcover = landcover.clip(polygon)

    connected_areas = get_connected_area(masked_landcover)

    largest_area_mask = get_largest_area_mask(connected_areas, polygon)

    largest_area_vector = largest_area_mask.reduceToVectors(
        geometryType='polygon',
        reducer=ee.Reducer.countEvery(),
        scale=FILTERING_AREAS_SCALE,
        maxPixels=1e13
    ).geometry().simplify(5)  # ).geometry().simplify(maxError=1)

    return largest_area_vector.coordinates().getInfo()


def calculate_polygons_difference(initial_polygon, filtered_polygon):
    """
    Function for defining coordinates of difference of 2 polygons
    :param initial_polygon:
    :param filtered_polygon:
    :return:
    """
    difference = initial_polygon.difference(filtered_polygon, ee.ErrorMargin(1))
    return difference.coordinates().getInfo()


def get_polygon_with_max_area(polygons):
    """
    Function for defining coordinates of polygon with the largest area inside the initail polygon
    :param polygons:
    :return:
    """
    polygons_data = [{'coords': coords, 'area': get_polygon_area(ee.Geometry.Polygon(coords))} for coords in polygons]
    result_polygon = max(polygons_data, key=lambda x: x['area'])
    return result_polygon['coords'] if result_polygon else None


def get_filtered_area_percent(polygon_area, filtered_area):
    """
    Function for obtaining the percentage ratio of the filtered area to the total area of the initial polygon
    :param polygon_area:
    :param filtered_area:
    :return:
    """
    return 100 * filtered_area / polygon_area


def get_classification_of_filtered_area(filtered_polygon):
    filtered_polygon_area = get_polygon_area(filtered_polygon)
    return get_area_classification_details(landcover, filtered_polygon, filtered_polygon_area)


def check_suitability_with_ai(prediction, filtered_polygon_data, polygon, coordinates, filtered_polygon_classification):
    """

    :param prediction:
    :param filtered_polygon_data:
    :param polygon:
    :param coordinates:
    :param filtered_polygon_classification:
    :return:
    """
    filtered_polygon = ee.Geometry.Polygon(filtered_polygon_data)

    if prediction < -0.5:
        landscape_prediction = predict_polygon(convert_polygon_stats(filtered_polygon_classification), model, scaler)
        if landscape_prediction > 0.5:
            return filtered_polygon.coordinates().getInfo()[0]
        elif landscape_prediction < -0.5:
            eligible_polygons = calculate_polygons_difference(polygon, filtered_polygon)
            max_polygon = get_polygon_with_max_area(eligible_polygons)
            return max_polygon[0]
        else:
            return []
    elif prediction > 0.3:
        return coordinates
    else:
        print('     !!! ', prediction)
        return []


def define_suitable_polygon_coordinates(prediction, filtered_polygon_data, polygon, coordinates):
    """

    :param prediction:
    :param filtered_polygon_data:
    :param polygon:
    :param coordinates:
    :return:
    """
    filtered_polygon = ee.Geometry.Polygon(filtered_polygon_data)
    filtered_polygon_classification = get_classification_of_filtered_area(filtered_polygon)
    check_of_suitable_types_filtered_result = check_suitable_types(filtered_polygon_classification)

    if len(check_of_suitable_types_filtered_result) == len(filtered_polygon_classification):
        return filtered_polygon.coordinates().getInfo()[0]
    else:
        return check_suitability_with_ai(prediction, filtered_polygon_data, polygon, coordinates,
                                         filtered_polygon_classification)


def check_suitable_types(land_types_stats):
    """

    :param land_types_stats:
    :return:
    """
    results = []

    for i in land_types_stats:
        if i['id'] in SUITABLE_TYPES:  # [30, 40, 60, 100]
            results.append(i)
    return results


def get_suitable_territory(coordinates, land_types_stats, polygon):
    check_of_suitable_types_result = check_suitable_types(land_types_stats)
    if len(check_of_suitable_types_result) == len(land_types_stats):
        print('ALL LANDTYPES ARE SUITABLE')
        return coordinates
    elif len(check_of_suitable_types_result) == 0:
        print('THERE ISNT ANY SUITABLE LANDTYPE')
        return []
    else:
        print('FINDING DIFFERENCE')
        landscape_prediction = predict_polygon(convert_polygon_stats(land_types_stats), model, scaler)

        print('PREDICTION: ', landscape_prediction)

        filtered_polygon_data = get_filtered_area_coordinates(polygon, landcover)

        return define_suitable_polygon_coordinates(landscape_prediction, filtered_polygon_data, polygon, coordinates)


def get_ee_classification(coordinates):
    """

    :param coordinates:
    :return:
    """
    polygon = ee.Geometry.Polygon(coordinates)

    polygon_area = get_polygon_area(polygon)

    if polygon_area < MIN_POLYGON_AREA:
        raise Exception(f'Minimal polygon area must be - {MIN_POLYGON_AREA} km^2, area of your polygon - {polygon_area} km^2')

    land_types_stats = get_area_classification_details(landcover, polygon, polygon_area)

    suitable_territory = get_suitable_territory(coordinates, land_types_stats, polygon)

    if suitable_territory and suitable_territory != []:
        suitable_territory_polygon = ee.Geometry.Polygon(suitable_territory)
        suitable_territory_area_km = get_polygon_area(suitable_territory_polygon)
        energy_output = get_energy_output_stats(coordinates[0], get_polygon_area_m2(suitable_territory_polygon))
        print(energy_output)
        return land_types_stats, suitable_territory, polygon_area, suitable_territory_area_km, energy_output
    return land_types_stats, suitable_territory, polygon_area, 0, {}
