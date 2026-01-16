from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Prediction
import json


@csrf_exempt
@require_http_methods(["POST"])
def prediction_view(request):
    try:
        data = json.loads(request.body)

        phone_number = data.get('phone_number')
        dropout = data.get('dropout')

        if phone_number is None:
            return JsonResponse({
                'success': False,
                'error': 'El parámetro phone_number es requerido'
            }, status=400)

        if dropout is None:
            return JsonResponse({
                'success': False,
                'error': 'El parámetro dropout es requerido'
            }, status=400)

        dropout = int(dropout)

        if dropout not in [0, 1]:
            return JsonResponse({
                'success': False,
                'error': 'El parámetro dropout debe ser 0 o 1'
            }, status=400)

        prediction = Prediction.objects.create(
            phone_number=phone_number,
            dropout=dropout
        )

        return JsonResponse({
            'success': True,
            'id': prediction.id,
            'phone_number': prediction.phone_number,
            'dropout': prediction.dropout,
            'message': 'estudiante fuga' if dropout == 1 else 'estudiante no fugará',
            'created_at': prediction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, status=201)

    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'El parámetro dropout debe ser un número entero'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
