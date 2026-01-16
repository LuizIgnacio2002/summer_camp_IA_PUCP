from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Prediction
import json
import pickle
import random
import os
import time

# Cargar el modelo al iniciar
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'dropout_prediction_model.pkl')
model = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✓ Modelo de predicción cargado exitosamente")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")

# Valores posibles para campos categóricos (para generar aleatorios)
CATEGORICAL_VALUES = {
    'code_module': ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF', 'GGG'],
    'code_presentation': ['2013J', '2014J', '2013B', '2014B'],
    'gender': ['M', 'F'],
    'region': [
        'East Anglian Region', 'Scotland', 'North Western Region',
        'South East Region', 'West Midlands Region', 'London Region',
        'South Region', 'Yorkshire Region', 'East Midlands Region',
        'North Region', 'South West Region', 'Wales', 'Ireland'
    ],
    'highest_education': [
        'HE Qualification', 'A Level or Equivalent',
        'Lower Than A Level', 'Post Graduate Qualification', 'No Formal quals'
    ],
    'imd_band': [
        '90-100%', '80-90%', '70-80%', '60-70%', '50-60%',
        '40-50%', '30-40%', '20-30%', '10-20%', '0-10%'
    ],
    'age_band': ['0-35', '35-55', '55<='],
    'disability': ['N', 'Y']
}


def generate_random_value(field_name):
    """Genera un valor aleatorio para un campo específico"""
    if field_name in CATEGORICAL_VALUES:
        return random.choice(CATEGORICAL_VALUES[field_name])
    
    # Valores numéricos con rangos apropiados
    numeric_defaults = {
        'phone_number': f"+51{random.randint(900000000, 999999999)}",
        'num_of_prev_attempts': random.randint(0, 6),
        'studied_credits': random.choice([30, 60, 90, 120, 150, 180, 210, 240]),
        'days_enrolled_until_90': round(random.uniform(0, 300), 1),
        'unreg_before_90': random.choice([0, 1]),
        'n_assess_submitted_early': float(random.randint(0, 8)),
        'mean_score_early': round(random.uniform(0, 100), 1),
        'n_assess_not_submitted_early': float(random.randint(0, 5)),
        'total_clicks_0_90': float(random.randint(0, 5000)),
        'active_days_0_90': float(random.randint(0, 90)),
        'dataplus': float(random.randint(0, 50)),
        'dualpane': float(random.randint(0, 30)),
        'externalquiz': float(random.randint(0, 20)),
        'forumng': float(random.randint(0, 500)),
        'glossary': float(random.randint(0, 20)),
        'homepage': float(random.randint(0, 300)),
        'htmlactivity': float(random.randint(0, 50)),
        'oucollaborate': float(random.randint(0, 30)),
        'oucontent': float(random.randint(0, 800)),
        'ouelluminate': float(random.randint(0, 20)),
        'ouwiki': float(random.randint(0, 100)),
        'page': float(random.randint(0, 50)),
        'questionnaire': float(random.randint(0, 30)),
        'quiz': float(random.randint(0, 200)),
        'repeatactivity': float(random.randint(0, 20)),
        'resource': float(random.randint(0, 50)),
        'sharedsubpage': float(random.randint(0, 20)),
        'subpage': float(random.randint(0, 150)),
        'url': float(random.randint(0, 100))
    }
    
    return numeric_defaults.get(field_name, 0.0)


def fill_missing_fields(data):
    """Completa los campos faltantes con valores aleatorios"""
    required_fields = [
        'phone_number', 'code_module', 'code_presentation', 'gender', 'region',
        'highest_education', 'imd_band', 'age_band', 'disability',
        'num_of_prev_attempts', 'studied_credits', 'days_enrolled_until_90',
        'unreg_before_90', 'n_assess_submitted_early', 'mean_score_early',
        'n_assess_not_submitted_early', 'total_clicks_0_90', 'active_days_0_90',
        'dataplus', 'dualpane', 'externalquiz', 'forumng', 'glossary',
        'homepage', 'htmlactivity', 'oucollaborate', 'oucontent', 'ouelluminate',
        'ouwiki', 'page', 'questionnaire', 'quiz', 'repeatactivity',
        'resource', 'sharedsubpage', 'subpage', 'url'
    ]
    
    filled_data = data.copy()
    generated_fields = []
    
    for field in required_fields:
        if field not in filled_data or filled_data[field] is None:
            filled_data[field] = generate_random_value(field)
            generated_fields.append(field)
    
    return filled_data, generated_fields


def prepare_features(data):
    """Prepara las características para el modelo en el orden correcto"""
    # Orden de las características que espera el modelo
    feature_order = [
        'code_module', 'code_presentation', 'gender', 'region',
        'highest_education', 'imd_band', 'age_band', 'disability',
        'num_of_prev_attempts', 'studied_credits', 'days_enrolled_until_90',
        'unreg_before_90', 'n_assess_submitted_early', 'mean_score_early',
        'n_assess_not_submitted_early', 'total_clicks_0_90', 'active_days_0_90',
        'dataplus', 'dualpane', 'externalquiz', 'forumng', 'glossary',
        'homepage', 'htmlactivity', 'oucollaborate', 'oucontent', 'ouelluminate',
        'ouwiki', 'page', 'questionnaire', 'quiz', 'repeatactivity',
        'resource', 'sharedsubpage', 'subpage', 'url'
    ]
    
    features = {key: data[key] for key in feature_order}
    return features


@csrf_exempt
@require_http_methods(["POST"])
def prediction_view(request):
    try:
        data = json.loads(request.body)
        
        # Completar campos faltantes con valores aleatorios
        filled_data, generated_fields = fill_missing_fields(data)
        
        phone_number = filled_data.get('phone_number')
        
        if model is None:
            return JsonResponse({
                'success': False,
                'error': 'Modelo de predicción no disponible'
            }, status=500)
        
        # Preparar características para el modelo
        start_time = time.perf_counter()
        
        try:
            import pandas as pd
            
            features = prepare_features(filled_data)
            df = pd.DataFrame([features])
            
            # Realizar predicción
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][1]
            
        except Exception as model_error:
            return JsonResponse({
                'success': False,
                'error': f'Error en predicción del modelo: {str(model_error)}'
            }, status=500)
        
        end_time = time.perf_counter()
        prediction_time = end_time - start_time
        
        # Determinar nivel de riesgo
        if probability < 0.3:
            risk_level = 'BAJO'
        elif probability < 0.7:
            risk_level = 'MEDIO'
        else:
            risk_level = 'ALTO'
        
        # Convertir predicción a entero (0 o 1)
        dropout = int(prediction)
        
        # Imprimir mensaje según la predicción
        if dropout == 1:
            print("=" * 50)
            print("⚠️  ESTUDIANTE PROPENSO A FUGA")
            print(f"   Teléfono: {phone_number}")
            print(f"   Probabilidad: {probability:.2%}")
            print(f"   Nivel de riesgo: {risk_level}")
            print("=" * 50)
        else:
            print("=" * 50)
            print("✓  NO HAY PROBLEMA CON EL ESTUDIANTE")
            print(f"   Teléfono: {phone_number}")
            print(f"   Probabilidad de abandono: {probability:.2%}")
            print(f"   Nivel de riesgo: {risk_level}")
            print("=" * 50)
        
        # Guardar en base de datos
        prediction_obj = Prediction.objects.create(
            phone_number=phone_number,
            dropout=dropout
        )
        
        response_data = {
            'success': True,
            'message': 'Predicción realizada exitosamente',
            'data': {
                'id': prediction_obj.id,
                'phone_number': phone_number,
                'prediction': 'ABANDONA' if dropout == 1 else 'NO ABANDONA',
                'message': 'estudiante propenso a fuga' if dropout == 1 else 'no hay problema con el estudiante',
                'dropout_probability': f"{probability:.2%}",
                'risk_level': risk_level,
                'prediction_time': f"{prediction_time:.4f}s"
            }
        }
        
        # Agregar información sobre campos generados aleatoriamente
        if generated_fields:
            response_data['data']['generated_fields'] = generated_fields
            response_data['data']['generated_fields_count'] = len(generated_fields)
        
        return JsonResponse(response_data, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido en el cuerpo de la solicitud'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_predictions_view(request):
    """Obtiene todas las predicciones almacenadas"""
    try:
        predictions = Prediction.objects.all()
        
        data = []
        for p in predictions:
            data.append({
                'id': p.id,
                'phone_number': p.phone_number,
                'prediction': 'ABANDONA' if p.dropout == 1 else 'NO ABANDONA',
                'risk_level': 'ALTO' if p.dropout == 1 else 'BAJO',
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
