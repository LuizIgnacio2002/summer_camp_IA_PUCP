from django.contrib import admin
from .models import Preguntas

# Register your models here.
class PreguntasAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'question1', 'question2', 'question3', 'question4', 'question5')
    search_fields = ('phone_number',)

admin.site.register(Preguntas, PreguntasAdmin)