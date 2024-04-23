from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from diploma_api import settings
from .utils import get_ee_classification


def map_view(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'index.html', context)


class AnalyzeArea(APIView):
    def post(self, request):
        # try:
            data = JSONParser().parse(request)
            coordinates = data.get('coordinates')
            if not coordinates:
                return JsonResponse({'error': 'Error getting polygon data from request'}, status=500)
            polygon_classification = get_ee_classification(coordinates)
            return JsonResponse({'coordinates': coordinates, 'classification': polygon_classification[0],
                                 'area': polygon_classification[1], 'crop': polygon_classification[2]}, status=200)
        # except Exception as e:
        #     return JsonResponse({'error': 'Error analysing polygon data' + str(e)}, status=500)
