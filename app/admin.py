from django.contrib import admin
from .models import Preguntas

# Register your models here.
@admin.register(Preguntas)
class PreguntasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'code_module',
        'gender',
        'age_band',
        'get_prediction_display',
        'get_probability_display',
        'get_risk_level_display',
        'created_at'
    )

    list_filter = (
        'risk_level',
        'prediction',
        'gender',
        'age_band',
        'code_module',
        'disability',
        'created_at'
    )

    search_fields = (
        'phone_number',
        'code_module',
        'region'
    )

    readonly_fields = (
        'prediction',
        'dropout_probability',
        'risk_level',
        'created_at',
        'updated_at'
    )

    fieldsets = (
        ('Información de Contacto', {
            'fields': ('phone_number',)
        }),
        ('Datos del Estudiante', {
            'fields': (
                'code_module',
                'code_presentation',
                'gender',
                'region',
                'highest_education',
                'imd_band',
                'age_band',
                'disability'
            )
        }),
        ('Datos Académicos', {
            'fields': (
                'num_of_prev_attempts',
                'studied_credits',
                'days_enrolled_until_90',
                'unreg_before_90'
            )
        }),
        ('Evaluaciones Tempranas', {
            'fields': (
                'n_assess_submitted_early',
                'mean_score_early',
                'n_assess_not_submitted_early'
            )
        }),
        ('Actividad General', {
            'fields': (
                'total_clicks_0_90',
                'active_days_0_90'
            )
        }),
        ('Clics por Tipo de Actividad', {
            'classes': ('collapse',),
            'fields': (
                'dataplus',
                'dualpane',
                'externalquiz',
                'forumng',
                'glossary',
                'homepage',
                'htmlactivity',
                'oucollaborate',
                'oucontent',
                'ouelluminate',
                'ouwiki',
                'page',
                'questionnaire',
                'quiz',
                'repeatactivity',
                'resource',
                'sharedsubpage',
                'subpage',
                'url'
            )
        }),
        ('Resultados de Predicción', {
            'fields': (
                'prediction',
                'dropout_probability',
                'risk_level'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at'
            )
        })
    )

    ordering = ('-created_at',)

    list_per_page = 25

    def get_prediction_display(self, obj):
        if obj.prediction is None:
            return '❓ Sin predicción'
        return '❌ ABANDONA' if obj.prediction == 1 else '✅ NO ABANDONA'
    get_prediction_display.short_description = 'Predicción'

    def get_probability_display(self, obj):
        if obj.dropout_probability is None:
            return '-'
        return f"{obj.dropout_probability:.2%}"
    get_probability_display.short_description = 'Prob. Abandono'

    def get_risk_level_display(self, obj):
        if not obj.risk_level:
            return '-'
        colors = {
            'BAJO': '🟢',
            'MEDIO': '🟡',
            'ALTO': '🔴'
        }
        return f"{colors.get(obj.risk_level, '')} {obj.risk_level}"
    get_risk_level_display.short_description = 'Nivel de Riesgo'