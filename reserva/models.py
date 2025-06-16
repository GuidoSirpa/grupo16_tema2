from django.db import models
from cliente.models import Cliente
from habitacion.models import Habitacion

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    numero_personas = models.PositiveIntegerField(default=1)  

    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('finalizada', 'Finalizada'),
    ], default='pendiente')
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cliente} - Habitación {self.habitacion.numero}'
