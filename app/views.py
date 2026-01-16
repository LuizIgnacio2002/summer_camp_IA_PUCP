from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Preguntas
import json
import pickle
import pandas as pd
import os
import time
import random

# Datos de ejemplo para valores por defecto aleatorios
SAMPLE_DATA = [
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'M', 'region': 'East Anglian Region',
        'highest_education': 'HE Qualification', 'imd_band': '90-100%', 'age_band': '55<=',
        'num_of_prev_attempts': 0, 'studied_credits': 240, 'disability': 'N',
        'days_enrolled_until_90': 249.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 81.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 587.0,
        'active_days_0_90': 23.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 126.0, 'glossary': 0.0, 'homepage': 80.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 348.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 9.0, 'sharedsubpage': 0.0, 'subpage': 23.0, 'url': 1.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'Scotland',
        'highest_education': 'HE Qualification', 'imd_band': '20-30%', 'age_band': '35-55',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 143.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 69.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 821.0,
        'active_days_0_90': 36.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 283.0, 'glossary': 0.0, 'homepage': 187.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 248.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 5.0, 'sharedsubpage': 0.0, 'subpage': 63.0, 'url': 35.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'North Western Region',
        'highest_education': 'A Level or Equivalent', 'imd_band': '30-40%', 'age_band': '35-55',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'Y',
        'days_enrolled_until_90': 182.0, 'unreg_before_90': 1, 'n_assess_submitted_early': 0.0,
        'mean_score_early': 0.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 281.0,
        'active_days_0_90': 12.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 126.0, 'glossary': 0.0, 'homepage': 59.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 66.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 4.0, 'sharedsubpage': 0.0, 'subpage': 22.0, 'url': 4.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'South East Region',
        'highest_education': 'A Level or Equivalent', 'imd_band': '50-60%', 'age_band': '35-55',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 142.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 71.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 992.0,
        'active_days_0_90': 51.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 260.0, 'glossary': 1.0, 'homepage': 217.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 383.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 10.0, 'sharedsubpage': 0.0, 'subpage': 81.0, 'url': 40.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'West Midlands Region',
        'highest_education': 'Lower Than A Level', 'imd_band': '50-60%', 'age_band': '0-35',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 266.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 49.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 684.0,
        'active_days_0_90': 35.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 160.0, 'glossary': 2.0, 'homepage': 126.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 350.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 7.0, 'sharedsubpage': 0.0, 'subpage': 33.0, 'url': 6.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'M', 'region': 'Wales',
        'highest_education': 'A Level or Equivalent', 'imd_band': '80-90%', 'age_band': '35-55',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 200.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 74.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 1060.0,
        'active_days_0_90': 58.0, 'dataplus': 7.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 461.0, 'glossary': 0.0, 'homepage': 253.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 275.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 6.0, 'sharedsubpage': 0.0, 'subpage': 41.0, 'url': 17.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'M', 'region': 'Scotland',
        'highest_education': 'HE Qualification', 'imd_band': '30-40%', 'age_band': '0-35',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 157.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 67.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 726.0,
        'active_days_0_90': 34.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 89.0, 'glossary': 0.0, 'homepage': 152.0, 'htmlactivity': 0.0,
        'oucollaborate': 2.0, 'oucontent': 399.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 7.0, 'sharedsubpage': 0.0, 'subpage': 63.0, 'url': 14.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'North Western Region',
        'highest_education': 'A Level or Equivalent', 'imd_band': '90-100%', 'age_band': '0-35',
        'num_of_prev_attempts': 0, 'studied_credits': 120, 'disability': 'N',
        'days_enrolled_until_90': 119.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 72.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 663.0,
        'active_days_0_90': 39.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 245.0, 'glossary': 0.0, 'homepage': 144.0, 'htmlactivity': 0.0,
        'oucollaborate': 1.0, 'oucontent': 189.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 4.0, 'sharedsubpage': 0.0, 'subpage': 55.0, 'url': 25.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'East Anglian Region',
        'highest_education': 'A Level or Equivalent', 'imd_band': '70-80%', 'age_band': '0-35',
        'num_of_prev_attempts': 0, 'studied_credits': 90, 'disability': 'N',
        'days_enrolled_until_90': 123.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 70.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 770.0,
        'active_days_0_90': 49.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 142.0, 'glossary': 0.0, 'homepage': 203.0, 'htmlactivity': 0.0,
        'oucollaborate': 2.0, 'oucontent': 285.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 3.0, 'sharedsubpage': 0.0, 'subpage': 87.0, 'url': 48.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'M', 'region': 'North Region',
        'highest_education': 'Post Graduate Qualification', 'imd_band': 'Unknown', 'age_band': '55<=',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 269.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 75.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 1242.0,
        'active_days_0_90': 55.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 661.0, 'glossary': 0.0, 'homepage': 166.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 319.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 4.0, 'sharedsubpage': 0.0, 'subpage': 56.0, 'url': 36.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'M', 'region': 'South Region',
        'highest_education': 'Lower Than A Level', 'imd_band': '70-80%', 'age_band': '35-55',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 193.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 72.0, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 778.0,
        'active_days_0_90': 45.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 7.0, 'glossary': 0.0, 'homepage': 204.0, 'htmlactivity': 0.0,
        'oucollaborate': 0.0, 'oucontent': 437.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 2.0, 'sharedsubpage': 0.0, 'subpage': 85.0, 'url': 43.0
    },
    {
        'code_module': 'AAA', 'code_presentation': '2013J', 'gender': 'F', 'region': 'East Anglian Region',
        'highest_education': 'A Level or Equivalent', 'imd_band': '20-30%', 'age_band': '0-35',
        'num_of_prev_attempts': 0, 'studied_credits': 60, 'disability': 'N',
        'days_enrolled_until_90': 137.0, 'unreg_before_90': 0, 'n_assess_submitted_early': 2.0,
        'mean_score_early': 73.5, 'n_assess_not_submitted_early': 0.0, 'total_clicks_0_90': 809.0,
        'active_days_0_90': 44.0, 'dataplus': 0.0, 'dualpane': 0.0, 'externalquiz': 0.0,
        'forumng': 167.0, 'glossary': 0.0, 'homepage': 212.0, 'htmlactivity': 0.0,
        'oucollaborate': 2.0, 'oucontent': 336.0, 'ouelluminate': 0.0, 'ouwiki': 0.0,
        'page': 0.0, 'questionnaire': 0.0, 'quiz': 0.0, 'repeatactivity': 0.0,
        'resource': 3.0, 'sharedsubpage': 0.0, 'subpage': 56.0, 'url': 33.0
    }
]

def get_random_default(field_name):
    """Obtiene un valor aleatorio para un campo de los datos de ejemplo"""
    random_sample = random.choice(SAMPLE_DATA)
    return random_sample.get(field_name)

# Cargar el modelo de predicción al iniciar el módulo
MODEL_PATH = 'dropout_prediction_model.pkl'
model = None

def load_model():
    """Carga el modelo de predicción de abandono estudiantil"""
    global model
    try:
        start_load = time.perf_counter()
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
        end_load = time.perf_counter()
        print(f"✓ Modelo cargado exitosamente en {end_load - start_load:.4f} segundos")
        return True
    except FileNotFoundError:
        print(f"ERROR: No se encontró el modelo en {MODEL_PATH}")
        return False
    except Exception as e:
        print(f"ERROR al cargar el modelo: {str(e)}")
        return False

# Cargar el modelo al iniciar
load_model()


@csrf_exempt
@require_http_methods(["POST"])
def crear_prediccion(request):
    """
    Endpoint para crear una predicción de abandono estudiantil.
    Recibe todos los datos del estudiante, los guarda en la BD,
    realiza la predicción usando el modelo pkl y devuelve el resultado.
    """
    try:
        # Verificar que el modelo esté cargado
        if model is None:
            return JsonResponse({
                'success': False,
                'error': 'Modelo de predicción no disponible'
            }, status=500)

        data = json.loads(request.body)

        # Crear el registro en la base de datos (sin predicción aún)
        # Si faltan campos, se usarán valores aleatorios de los datos de ejemplo
        estudiante = Preguntas.objects.create(
            phone_number=data.get('phone_number', ''),
            code_module=data.get('code_module', get_random_default('code_module')),
            code_presentation=data.get('code_presentation', get_random_default('code_presentation')),
            gender=data.get('gender', get_random_default('gender')),
            region=data.get('region', get_random_default('region')),
            highest_education=data.get('highest_education', get_random_default('highest_education')),
            imd_band=data.get('imd_band', get_random_default('imd_band')),
            age_band=data.get('age_band', get_random_default('age_band')),
            disability=data.get('disability', get_random_default('disability')),
            num_of_prev_attempts=data.get('num_of_prev_attempts', get_random_default('num_of_prev_attempts')),
            studied_credits=data.get('studied_credits', get_random_default('studied_credits')),
            days_enrolled_until_90=data.get('days_enrolled_until_90', get_random_default('days_enrolled_until_90')),
            unreg_before_90=data.get('unreg_before_90', get_random_default('unreg_before_90')),
            n_assess_submitted_early=float(data.get('n_assess_submitted_early', get_random_default('n_assess_submitted_early'))),
            mean_score_early=float(data.get('mean_score_early', get_random_default('mean_score_early'))),
            n_assess_not_submitted_early=float(data.get('n_assess_not_submitted_early', get_random_default('n_assess_not_submitted_early'))),
            total_clicks_0_90=float(data.get('total_clicks_0_90', get_random_default('total_clicks_0_90'))),
            active_days_0_90=float(data.get('active_days_0_90', get_random_default('active_days_0_90'))),
            dataplus=float(data.get('dataplus', get_random_default('dataplus'))),
            dualpane=float(data.get('dualpane', get_random_default('dualpane'))),
            externalquiz=float(data.get('externalquiz', get_random_default('externalquiz'))),
            forumng=float(data.get('forumng', get_random_default('forumng'))),
            glossary=float(data.get('glossary', get_random_default('glossary'))),
            homepage=float(data.get('homepage', get_random_default('homepage'))),
            htmlactivity=float(data.get('htmlactivity', get_random_default('htmlactivity'))),
            oucollaborate=float(data.get('oucollaborate', get_random_default('oucollaborate'))),
            oucontent=float(data.get('oucontent', get_random_default('oucontent'))),
            ouelluminate=float(data.get('ouelluminate', get_random_default('ouelluminate'))),
            ouwiki=float(data.get('ouwiki', get_random_default('ouwiki'))),
            page=float(data.get('page', get_random_default('page'))),
            questionnaire=float(data.get('questionnaire', get_random_default('questionnaire'))),
            quiz=float(data.get('quiz', get_random_default('quiz'))),
            repeatactivity=float(data.get('repeatactivity', get_random_default('repeatactivity'))),
            resource=float(data.get('resource', get_random_default('resource'))),
            sharedsubpage=float(data.get('sharedsubpage', get_random_default('sharedsubpage'))),
            subpage=float(data.get('subpage', get_random_default('subpage'))),
            url=float(data.get('url', get_random_default('url')))
        )

        # Preparar datos para la predicción
        student_data = {
            'code_module': [estudiante.code_module],
            'code_presentation': [estudiante.code_presentation],
            'gender': [estudiante.gender],
            'region': [estudiante.region],
            'highest_education': [estudiante.highest_education],
            'imd_band': [estudiante.imd_band],
            'age_band': [estudiante.age_band],
            'disability': [estudiante.disability],
            'num_of_prev_attempts': [estudiante.num_of_prev_attempts],
            'studied_credits': [estudiante.studied_credits],
            'days_enrolled_until_90': [estudiante.days_enrolled_until_90],
            'unreg_before_90': [estudiante.unreg_before_90],
            'n_assess_submitted_early': [estudiante.n_assess_submitted_early],
            'mean_score_early': [estudiante.mean_score_early],
            'n_assess_not_submitted_early': [estudiante.n_assess_not_submitted_early],
            'total_clicks_0_90': [estudiante.total_clicks_0_90],
            'active_days_0_90': [estudiante.active_days_0_90],
            'dataplus': [estudiante.dataplus],
            'dualpane': [estudiante.dualpane],
            'externalquiz': [estudiante.externalquiz],
            'forumng': [estudiante.forumng],
            'glossary': [estudiante.glossary],
            'homepage': [estudiante.homepage],
            'htmlactivity': [estudiante.htmlactivity],
            'oucollaborate': [estudiante.oucollaborate],
            'oucontent': [estudiante.oucontent],
            'ouelluminate': [estudiante.ouelluminate],
            'ouwiki': [estudiante.ouwiki],
            'page': [estudiante.page],
            'questionnaire': [estudiante.questionnaire],
            'quiz': [estudiante.quiz],
            'repeatactivity': [estudiante.repeatactivity],
            'resource': [estudiante.resource],
            'sharedsubpage': [estudiante.sharedsubpage],
            'subpage': [estudiante.subpage],
            'url': [estudiante.url]
        }

        df_student = pd.DataFrame(student_data)

        # Realizar predicción
        start_pred = time.perf_counter()
        prediction = model.predict(df_student)[0]
        probability = model.predict_proba(df_student)[0, 1]
        end_pred = time.perf_counter()
        pred_time = end_pred - start_pred

        # Determinar nivel de riesgo
        if probability < 0.3:
            risk_level = 'BAJO'
        elif probability < 0.7:
            risk_level = 'MEDIO'
        else:
            risk_level = 'ALTO'

        # Actualizar el registro con la predicción
        estudiante.prediction = int(prediction)
        estudiante.dropout_probability = float(probability)
        estudiante.risk_level = risk_level
        estudiante.save()

        return JsonResponse({
            'success': True,
            'message': 'Predicción realizada exitosamente',
            'data': {
                'id': estudiante.id,
                'phone_number': estudiante.phone_number,
                'prediction': 'ABANDONA' if prediction == 1 else 'NO ABANDONA',
                'dropout_probability': f"{probability:.2%}",
                'risk_level': risk_level,
                'prediction_time': f"{pred_time:.4f}s"
            }
        }, status=201)

    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Campo requerido faltante: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def obtener_predicciones(request):
    """
    Endpoint para obtener todas las predicciones realizadas.
    """
    try:
        predicciones = Preguntas.objects.all().order_by('-created_at')

        data = [{
            'id': p.id,
            'phone_number': p.phone_number,
            'code_module': p.code_module,
            'gender': p.gender,
            'age_band': p.age_band,
            'prediction': 'ABANDONA' if p.prediction == 1 else 'NO ABANDONA' if p.prediction is not None else 'Sin predicción',
            'dropout_probability': f"{p.dropout_probability:.2%}" if p.dropout_probability else None,
            'risk_level': p.risk_level,
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for p in predicciones]

        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
