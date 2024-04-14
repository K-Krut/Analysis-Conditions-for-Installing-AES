from django.urls import path
from .views import map_view, AnalyzeArea

urlpatterns = [
    path('test/', map_view, name='map'),
    path('api/polygon/', AnalyzeArea.as_view()),
]
