from django.urls import path
from . import views

urlpatterns = [
    path('prediccion/', views.prediction_view, name='prediction'),
    path('predicciones/', views.get_predictions_view, name='get_predictions'),
]
