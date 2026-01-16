# API de Predicción de Abandono Estudiantil

## Descripción

Esta API permite realizar predicciones sobre la probabilidad de abandono de estudiantes utilizando un modelo de Machine Learning entrenado. La API recibe datos del estudiante, los guarda en la base de datos, realiza la predicción y devuelve el resultado con el nivel de riesgo.

## Instalación y Configuración

### 1. Realizar las migraciones de la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Crear un superusuario para acceder al admin (opcional)

```bash
python manage.py createsuperuser
```

### 3. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## Endpoints Disponibles

### 1. Crear Predicción

**POST** `/app/prediccion/`

Crea una nueva predicción de abandono estudiantil.

**Request Body:**
```json
{
  "phone_number": "+51987654321",
  "code_module": "AAA",
  "code_presentation": "2013J",
  "gender": "M",
  "region": "East Anglian Region",
  "highest_education": "HE Qualification",
  "imd_band": "90-100%",
  "age_band": "0-35",
  "disability": "N",
  "num_of_prev_attempts": 0,
  "studied_credits": 240,
  "days_enrolled_until_90": 150.5,
  "unreg_before_90": 0,
  "n_assess_submitted_early": 5.0,
  "mean_score_early": 75.5,
  "n_assess_not_submitted_early": 1.0,
  "total_clicks_0_90": 1500.0,
  "active_days_0_90": 45.0,
  "dataplus": 25.0,
  "dualpane": 10.0,
  "externalquiz": 15.0,
  "forumng": 250.0,
  "glossary": 8.0,
  "homepage": 150.0,
  "htmlactivity": 30.0,
  "oucollaborate": 12.0,
  "oucontent": 400.0,
  "ouelluminate": 5.0,
  "ouwiki": 50.0,
  "page": 20.0,
  "questionnaire": 15.0,
  "quiz": 100.0,
  "repeatactivity": 8.0,
  "resource": 25.0,
  "sharedsubpage": 10.0,
  "subpage": 75.0,
  "url": 50.0
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Predicción realizada exitosamente",
  "data": {
    "id": 1,
    "phone_number": "+51987654321",
    "prediction": "NO ABANDONA",
    "dropout_probability": "25.50%",
    "risk_level": "BAJO",
    "prediction_time": "0.0023s"
  }
}
```

### 2. Obtener Predicciones

**GET** `/app/predicciones/`

Obtiene todas las predicciones realizadas.

**Response (200 OK):**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "phone_number": "+51987654321",
      "code_module": "AAA",
      "gender": "M",
      "age_band": "0-35",
      "prediction": "NO ABANDONA",
      "dropout_probability": "25.50%",
      "risk_level": "BAJO",
      "created_at": "2026-01-16 10:30:45"
    }
  ]
}
```

## Valores Válidos para Campos Categóricos

### code_module
`'AAA'`, `'BBB'`, `'CCC'`, `'DDD'`, `'EEE'`, `'FFF'`, `'GGG'`

### code_presentation
`'2013J'`, `'2014J'`, `'2013B'`, `'2014B'`

### gender
`'M'` (Masculino), `'F'` (Femenino)

### region
- `'East Anglian Region'`
- `'Scotland'`
- `'North Western Region'`
- `'South East Region'`
- `'West Midlands Region'`
- `'London Region'`
- `'South Region'`
- `'Yorkshire Region'`
- `'East Midlands Region'`
- `'North Region'`
- `'South West Region'`
- `'Wales'`
- `'Ireland'`

### highest_education
- `'HE Qualification'`
- `'A Level or Equivalent'`
- `'Lower Than A Level'`
- `'Post Graduate Qualification'`
- `'No Formal quals'`

### imd_band
`'90-100%'`, `'80-90%'`, `'70-80%'`, `'60-70%'`, `'50-60%'`, `'40-50%'`, `'30-40%'`, `'20-30%'`, `'10-20%'`, `'0-10%'`

### age_band
`'0-35'`, `'35-55'`, `'55<='`

### disability
`'Y'` (Sí), `'N'` (No)

### unreg_before_90
`0` (No), `1` (Sí)

## Niveles de Riesgo

La API calcula automáticamente el nivel de riesgo basado en la probabilidad de abandono:

- **BAJO**: Probabilidad < 30%
- **MEDIO**: Probabilidad 30% - 70%
- **ALTO**: Probabilidad > 70%

## Panel de Administración

Accede al panel de administración de Django en: `http://localhost:8000/admin/`

En el panel podrás:
- Ver todas las predicciones realizadas
- Filtrar por nivel de riesgo, género, edad, etc.
- Buscar por número de teléfono o código de módulo
- Ver estadísticas detalladas de cada estudiante

## Probar la API

### Opción 1: Script de prueba Python

Ejecuta el script de prueba incluido:

```bash
python app/test_api.py
```

Este script generará 5 estudiantes con datos aleatorios y realizará predicciones.

### Opción 2: cURL

```bash
curl -X POST http://localhost:8000/app/prediccion/ \
  -H "Content-Type: application/json" \
  -d @app/ejemplo_request.json
```

### Opción 3: Postman o Insomnia

Importa el archivo `ejemplo_request.json` como ejemplo de request body.

## Modelo de Machine Learning

El modelo se carga automáticamente al iniciar Django desde el archivo:
```
app/dropout_prediction_model.pkl
```

El modelo utiliza todas las características del estudiante para predecir:
- Si el estudiante abandonará (1) o no (0)
- La probabilidad de abandono (0.0 - 1.0)
- El nivel de riesgo (BAJO, MEDIO, ALTO)

## Estructura de la Base de Datos

El modelo `Preguntas` almacena:
- **Información de contacto**: phone_number
- **Datos categóricos**: módulo, presentación, género, región, educación, etc.
- **Datos numéricos**: intentos previos, créditos, días matriculado, etc.
- **Evaluaciones**: número de evaluaciones enviadas, puntuaciones, etc.
- **Actividad**: clics totales, días activos, actividad por tipo
- **Resultados**: predicción, probabilidad de abandono, nivel de riesgo
- **Timestamps**: created_at, updated_at

## Troubleshooting

### Error: "Modelo de predicción no disponible"

Verifica que el archivo `dropout_prediction_model.pkl` existe en el directorio `app/`.

### Error de conexión en test_api.py

Asegúrate de que el servidor Django esté corriendo:
```bash
python manage.py runserver
```

### Error en migraciones

Elimina las migraciones previas y vuelve a crearlas:
```bash
python manage.py migrate app zero
python manage.py makemigrations
python manage.py migrate
```
