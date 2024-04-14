from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from diploma_api import settings


def map_view(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'index.html', context)


class AnalyzeArea(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        coordinates = data.get('coordinates')
        print(coordinates)
        return JsonResponse({'status': 'success', 'coordinates': coordinates})