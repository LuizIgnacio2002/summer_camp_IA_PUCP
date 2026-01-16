from django.urls import path
from . import views

urlpatterns = [
    path('preguntas/', views.crear_preguntas, name='crear_preguntas'),
]
