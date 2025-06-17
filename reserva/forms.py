from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    """Formulario para usuarios normales: no incluye el campo cliente."""
    class Meta:
        model = Reserva
        fields = ['habitacion', 'fecha_entrada', 'fecha_salida', 'numero_personas']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class ReservaFormAdmin(forms.ModelForm):
    """Formulario para admin: permite elegir el cliente."""
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'numero_personas']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }