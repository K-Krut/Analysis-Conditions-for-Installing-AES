from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .utils import get_ee_classification, get_solar_energy_output_prediction


class AnalyzeArea(APIView):
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            coordinates = data.get('coordinates')
            if not coordinates:
                return JsonResponse({'error': 'Error getting polygon data from request'}, status=500)
            if len(coordinates) < 3:
                return JsonResponse({'error': 'Error - polygon must consist of at least 3 interconnected points'}, status=400)
            landscape_res = get_ee_classification(coordinates)
            energy_output = get_solar_energy_output_prediction(coordinates[0], landscape_res['crop']) if landscape_res['crop'] else {}
            return JsonResponse(
                {
                    'coordinates': coordinates,
                    'area': landscape_res['area'],
                    'crop': landscape_res['crop'],
                    'initial_polygon_area': landscape_res['initial_polygon_area'],
                    'suitable_polygon_area': landscape_res['suitable_polygon_area'],
                    'energy_output_stats': energy_output,
                },
                status=200
            )
        except Exception as e:
            return JsonResponse({'error': 'Error analysing polygon data' + str(e)}, status=500)
