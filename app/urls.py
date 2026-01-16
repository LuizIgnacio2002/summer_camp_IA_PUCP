from django.urls import path
from . import views

urlpatterns = [
    path('prediccion/', views.crear_prediccion, name='crear_prediccion'),
    path('predicciones/', views.obtener_predicciones, name='obtener_predicciones'),
]
