from django.db import models


class Prediction(models.Model):
    phone_number = models.CharField(max_length=15)
    dropout = models.IntegerField(choices=[(0, 'No abandona'), (1, 'Abandona')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone_number} - {'Abandona' if self.dropout == 1 else 'No abandona'}"
