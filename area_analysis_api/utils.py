import ee

from .constants import landscape_types, COPERNICUS_CROP_CLASS_ID, FILTERING_AREAS_SCALE
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
                'Percentage': round(percentage, 2),
                'id': land_type
            }

    # print(sum(value['Percentage'] for key, value in results.items() if value['Percentage'] > 0))
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
    class_mask_200 = masked_landcover.eq(200)
    combined_mask = class_mask_40.Or(class_mask_60).Or(class_mask_200).Or(class_mask_100)
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


def define_suitable_polygon_coordinates(polygon_area, filtered_polygon_data, polygon):
    filtered_polygon = ee.Geometry.Polygon(filtered_polygon_data)
    filtered_area = get_polygon_area(filtered_polygon)
    area_percent = get_filtered_area_percent(polygon_area, filtered_area)
    print('*' * 150)
    print('filtered_polygon_data    ', filtered_polygon_data)
    print('*' * 150)
    print(filtered_polygon.coordinates().getInfo())
    print('*' * 150)
    print(polygon)
    print('*' * 150)
    print('area_percent ', area_percent)
    print('*' * 150)
    if 80 < area_percent < 90:
        return filtered_polygon.coordinates().getInfo() if filtered_polygon and filtered_polygon.coordinates() else None
    elif area_percent > 90:
        return polygon
    else:
        eligible_polygons = calculate_polygons_difference(polygon, ee.Geometry.Polygon(filtered_polygon_data))
        return get_polygon_with_max_area(eligible_polygons)


def get_ee_classification(coordinates):
    polygon = ee.Geometry.Polygon(coordinates)
    landcover = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019").select('discrete_classification')
    print(coordinates)
    polygon_area = get_polygon_area(polygon)

    land_types_stats = get_area_classification_details(landcover, polygon, polygon_area)
    print(land_types_stats)

    filtered_polygon_data = get_filtered_area_coordinates(polygon, landcover)

    suitable_territory = define_suitable_polygon_coordinates(polygon_area, filtered_polygon_data, coordinates)

    return land_types_stats, suitable_territory
