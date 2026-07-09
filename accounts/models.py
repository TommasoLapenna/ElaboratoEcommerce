from django.contrib.auth.models import AbstractUser
from django.db import models

# Estensione della classe user di Django, per creare un custom user
# Invece che con valore booleano, l'assegnazione del ruole funziona tramite un enum, in modo da essere facilmente estendibile
class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('manager', 'Store Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username