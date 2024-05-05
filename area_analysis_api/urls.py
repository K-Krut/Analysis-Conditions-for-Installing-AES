from django.urls import path
from .views import AnalyzeArea

urlpatterns = [
    path('api/polygon/', AnalyzeArea.as_view()),
]
