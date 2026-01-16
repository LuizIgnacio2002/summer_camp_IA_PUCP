from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Preguntas
import json


@csrf_exempt
@require_http_methods(["POST"])
def crear_preguntas(request):
    """
    Endpoint para crear un nuevo registro de Preguntas.
    """
    try:
        data = json.loads(request.body)
        
        pregunta = Preguntas.objects.create(
            phone_number=data['phone_number'],
            question1=data['question1'],
            question2=data['question2'],
            question3=data['question3'],
            question4=data['question4'],
            question5=data['question5']
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Preguntas creadas exitosamente',
            'id': pregunta.id
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
