from django.db import models
from django.contrib.auth.models import User
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    perfil_confirmado = models.BooleanField(default=False)  # NUEVO CAMPO

    def __str__(self):
        return f"{self.nombre} {self.apellido}"