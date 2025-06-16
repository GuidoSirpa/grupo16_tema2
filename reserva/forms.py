from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # No incluyas 'cliente', se asigna automáticamente en la vista
        fields = ['habitacion', 'fecha_entrada', 'fecha_salida', 'numero_personas']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }