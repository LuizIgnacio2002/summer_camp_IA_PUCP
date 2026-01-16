"""
Script de prueba para la API de predicción de abandono estudiantil
Genera datos de ejemplo con valores random similares al dataset real
y los envía a la API de Django para realizar predicciones.
"""

import requests
import random
import json
import time

# Configuración
API_URL = 'http://localhost:8000/app/prediccion/'
API_GET_URL = 'http://localhost:8000/app/predicciones/'

# Valores posibles para cada columna categórica
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


def generate_random_student_data():
    """Genera datos aleatorios de un estudiante"""
    return {
        'phone_number': f"+51{random.randint(900000000, 999999999)}",
        'code_module': random.choice(CATEGORICAL_VALUES['code_module']),
        'code_presentation': random.choice(CATEGORICAL_VALUES['code_presentation']),
        'gender': random.choice(CATEGORICAL_VALUES['gender']),
        'region': random.choice(CATEGORICAL_VALUES['region']),
        'highest_education': random.choice(CATEGORICAL_VALUES['highest_education']),
        'imd_band': random.choice(CATEGORICAL_VALUES['imd_band']),
        'age_band': random.choice(CATEGORICAL_VALUES['age_band']),
        'disability': random.choice(CATEGORICAL_VALUES['disability']),
        'num_of_prev_attempts': random.randint(0, 6),
        'studied_credits': random.choice([30, 60, 90, 120, 150, 180, 210, 240]),
        'days_enrolled_until_90': round(random.uniform(0, 300), 1),
        'unreg_before_90': random.choice([0, 1]),
        'n_assess_submitted_early': float(random.randint(0, 8)),
        'mean_score_early': round(random.uniform(0, 100), 1) if random.random() > 0.3 else 0.0,
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


def test_prediccion():
    """Prueba el endpoint de predicción"""
    print("=" * 80)
    print("PRUEBA DE API DE PREDICCIÓN DE ABANDONO ESTUDIANTIL")
    print("=" * 80)
    print()

    n_students = 5
    print(f"Generando {n_students} estudiantes con datos aleatorios...")
    print()

    results = []

    for i in range(n_students):
        student_data = generate_random_student_data()

        print(f"\n--- Estudiante {i + 1} ---")
        print(f"Teléfono: {student_data['phone_number']}")
        print(f"Módulo: {student_data['code_module']}")
        print(f"Género: {student_data['gender']}")
        print(f"Edad: {student_data['age_band']}")

        try:
            start_time = time.perf_counter()
            response = requests.post(
                API_URL,
                json=student_data,
                headers={'Content-Type': 'application/json'}
            )
            end_time = time.perf_counter()
            request_time = end_time - start_time

            if response.status_code == 201:
                result = response.json()
                if result['success']:
                    data = result['data']
                    print(f"✓ Predicción exitosa (Tiempo total: {request_time:.4f}s)")
                    print(f"  ID: {data['id']}")
                    print(f"  Predicción: {data['prediction']}")
                    print(f"  Probabilidad: {data['dropout_probability']}")
                    print(f"  Nivel de Riesgo: {data['risk_level']}")
                    print(f"  Tiempo de predicción: {data['prediction_time']}")
                    results.append(data)
                else:
                    print(f"✗ Error: {result['error']}")
            else:
                print(f"✗ Error HTTP {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            print("✗ Error: No se pudo conectar al servidor Django")
            print("  Asegúrate de que el servidor esté corriendo con: python manage.py runserver")
            return
        except Exception as e:
            print(f"✗ Error inesperado: {str(e)}")

    print("\n" + "=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    print(f"\n{'#':<3} {'Teléfono':<15} {'Predicción':<15} {'Probabilidad':<15} {'Riesgo':<10}")
    print("-" * 80)

    for i, result in enumerate(results, 1):
        print(f"{i:<3} {result['phone_number']:<15} {result['prediction']:<15} "
              f"{result['dropout_probability']:<15} {result['risk_level']:<10}")

    print("\n" + "=" * 80)
    print(f"Predicciones realizadas exitosamente: {len(results)}/{n_students}")
    print("=" * 80)


def test_obtener_predicciones():
    """Prueba el endpoint para obtener todas las predicciones"""
    print("\n" + "=" * 80)
    print("OBTENIENDO TODAS LAS PREDICCIONES")
    print("=" * 80)

    try:
        response = requests.get(API_GET_URL)

        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"\n✓ Total de predicciones en BD: {result['count']}")

                if result['count'] > 0:
                    print("\nÚltimas 5 predicciones:")
                    print("-" * 80)
                    for prediccion in result['data'][:5]:
                        print(f"ID: {prediccion['id']} | "
                              f"Tel: {prediccion['phone_number']} | "
                              f"Pred: {prediccion['prediction']} | "
                              f"Riesgo: {prediccion['risk_level']}")
            else:
                print(f"✗ Error: {result['error']}")
        else:
            print(f"✗ Error HTTP {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar al servidor Django")
    except Exception as e:
        print(f"✗ Error inesperado: {str(e)}")


if __name__ == '__main__':
    print("\n🚀 Iniciando pruebas de API...\n")

    test_prediccion()

    print("\n" + "=" * 80)
    input("\nPresiona ENTER para obtener todas las predicciones...")

    test_obtener_predicciones()

    print("\n✅ Pruebas completadas\n")
