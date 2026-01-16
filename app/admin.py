from django.contrib import admin
from .models import Prediction

# Register your models here.
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'get_dropout_display',
        'created_at'
    )

    list_filter = (
        'dropout',
        'created_at'
    )

    search_fields = (
        'phone_number',
    )

    readonly_fields = (
        'created_at',
    )

    fieldsets = (
        ('Información de Contacto', {
            'fields': ('phone_number',)
        }),
        ('Predicción', {
            'fields': ('dropout',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )

    ordering = ('-created_at',)

    list_per_page = 25

    def get_dropout_display(self, obj):
        return '❌ ABANDONA' if obj.dropout == 1 else '✅ NO ABANDONA'
    get_dropout_display.short_description = 'Estado'