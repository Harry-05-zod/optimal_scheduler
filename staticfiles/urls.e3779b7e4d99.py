# dashboard/urls.py
from django.urls import path
from .views import HomeView, InsightsView, PredictionView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('insights/', InsightsView.as_view(), name='insights'),
    path('predict/', PredictionView.as_view(), name='prediction'),
]