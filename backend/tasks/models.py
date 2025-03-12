# tasks/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendiente'),
        ('IP', 'En progreso'),
        ('C', 'Completada')
    ]
    
    PRIORITY_CHOICES = [
        ('L', 'Baja'),
        ('M', 'Media'),
        ('H', 'Alta')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

