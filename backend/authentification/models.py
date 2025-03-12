# authentification/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Campo para la foto de perfil

    # Agrega related_name para evitar colisiones con el modelo auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='authentification_user_groups',  # Nombre personalizado
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='authentification_user_permissions',  # Nombre personalizado
        blank=True
    )

    def __str__(self):
        return self.username


