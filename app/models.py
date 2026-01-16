from django.db import models

# Create your models here.

class Preguntas(models.Model):
    phone_number = models.CharField(max_length=15)
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    question3 = models.CharField(max_length=255)
    question4 = models.CharField(max_length=255)
    question5 = models.CharField(max_length=255)

    def __str__(self):
        return f"Preguntas de {self.phone_number}"