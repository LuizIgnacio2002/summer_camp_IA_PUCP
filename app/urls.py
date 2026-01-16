from django.urls import path
from . import views

urlpatterns = [
    path('api/prediction/', views.prediction_view, name='prediction'),
]
