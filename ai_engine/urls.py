from django.urls import path
from . import views

urlpatterns = [
    path('api/strategy/', views.generate_strategy, name='generate_strategy'),
    path('api/analyze-image/', views.analyze_competitor_image, name='analyze_image'),
]