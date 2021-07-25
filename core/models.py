# core/models.py
from django.db import models


class TODO(models.Model):
    name = models.CharField(max_length=100, unique=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
