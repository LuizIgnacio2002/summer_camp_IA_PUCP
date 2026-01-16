from django.db import models

# Create your models here.

class Preguntas(models.Model):
    # Información de contacto
    phone_number = models.CharField(max_length=15)

    # Datos categóricos del estudiante
    code_module = models.CharField(max_length=10, help_text="Código del módulo")
    code_presentation = models.CharField(max_length=10, help_text="Código de presentación")
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    region = models.CharField(max_length=100, help_text="Región del estudiante")
    highest_education = models.CharField(max_length=100, help_text="Nivel educativo más alto")
    imd_band = models.CharField(max_length=20, help_text="Banda de índice de privación múltiple")
    age_band = models.CharField(max_length=10, help_text="Rango de edad")
    disability = models.CharField(max_length=1, choices=[('Y', 'Sí'), ('N', 'No')])

    # Datos numéricos del estudiante
    num_of_prev_attempts = models.IntegerField(default=0, help_text="Número de intentos previos")
    studied_credits = models.IntegerField(help_text="Créditos estudiados")
    days_enrolled_until_90 = models.FloatField(help_text="Días matriculado hasta día 90")
    unreg_before_90 = models.IntegerField(choices=[(0, 'No'), (1, 'Sí')], help_text="Desmatriculado antes del día 90")

    # Evaluaciones tempranas
    n_assess_submitted_early = models.FloatField(default=0.0, help_text="Número de evaluaciones enviadas temprano")
    mean_score_early = models.FloatField(default=0.0, help_text="Puntuación media temprana")
    n_assess_not_submitted_early = models.FloatField(default=0.0, help_text="Evaluaciones no enviadas temprano")

    # Actividad general
    total_clicks_0_90 = models.FloatField(default=0.0, help_text="Total de clics días 0-90")
    active_days_0_90 = models.FloatField(default=0.0, help_text="Días activos 0-90")

    # Clics por tipo de actividad
    dataplus = models.FloatField(default=0.0)
    dualpane = models.FloatField(default=0.0)
    externalquiz = models.FloatField(default=0.0)
    forumng = models.FloatField(default=0.0)
    glossary = models.FloatField(default=0.0)
    homepage = models.FloatField(default=0.0)
    htmlactivity = models.FloatField(default=0.0)
    oucollaborate = models.FloatField(default=0.0)
    oucontent = models.FloatField(default=0.0)
    ouelluminate = models.FloatField(default=0.0)
    ouwiki = models.FloatField(default=0.0)
    page = models.FloatField(default=0.0)
    questionnaire = models.FloatField(default=0.0)
    quiz = models.FloatField(default=0.0)
    repeatactivity = models.FloatField(default=0.0)
    resource = models.FloatField(default=0.0)
    sharedsubpage = models.FloatField(default=0.0)
    subpage = models.FloatField(default=0.0)
    url = models.FloatField(default=0.0)

    # Resultados de predicción
    prediction = models.IntegerField(null=True, blank=True, help_text="Predicción: 1=Abandona, 0=No abandona")
    dropout_probability = models.FloatField(null=True, blank=True, help_text="Probabilidad de abandono")
    risk_level = models.CharField(max_length=10, null=True, blank=True, help_text="Nivel de riesgo: BAJO, MEDIO, ALTO")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Predicción de Abandono"
        verbose_name_plural = "Predicciones de Abandono"
        ordering = ['-created_at']

    def __str__(self):
        return f"Estudiante {self.phone_number} - {self.code_module} ({self.risk_level if self.risk_level else 'Sin predicción'})"