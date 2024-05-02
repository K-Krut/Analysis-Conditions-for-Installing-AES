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
            if len(coordinates) < 3:
                return JsonResponse({'error': 'Error - polygon must consist of at least 3 interconnected points'}, status=500)
            res = get_ee_classification(coordinates)
            return JsonResponse({'coordinates': coordinates, 'area': res[0], 'crop': res[1], 'f': res[2], 'e': res[3]}, status=200)
        # except Exception as e:
        #     return JsonResponse({'error': 'Error analysing polygon data' + str(e)}, status=500)
