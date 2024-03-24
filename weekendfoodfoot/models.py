from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models

class TableType(models.Model):
    TYPE_CHOICES = [
        ('COUPLE', 'Couple'),
        ('FAMILIAL', 'Familial'),
        ('INDIVIDUAL', 'Individuel'),
        ('VIP', 'VIP'),
        ('EXTRA_FAMILLE', 'Extra Famille'),
        ('FAMILIAL_MIXTE', 'Famille Mixte'),
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    seats = models.IntegerField(default=2)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_path = models.CharField(max_length=100, default='path/to/default/image.jpg')  # Chemin vers l'image

    def __str__(self):
        return f"{self.get_name_display()} ({self.seats} places)"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'table_type', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.table_type} - {self.date}"
