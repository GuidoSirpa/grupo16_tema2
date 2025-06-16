from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from habitacion.models import Habitacion
from datetime import datetime
from django.db.models import Q
from tipo_habitacion.models import TipoHabitacion

def index(request):
    habitaciones_disponibles = None
    tipos_habitacion = TipoHabitacion.objects.all()

    if request.method == 'POST':
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')
        tipo_id = request.POST.get('tipo_habitacion')

        if fecha_entrada and fecha_salida and tipo_id:
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()
            habitaciones = Habitacion.objects.filter(tipo_id=tipo_id)
            disponibles = []
            for hab in habitaciones:
                hay_reserva = Reserva.objects.filter(
                    habitacion=hab,
                    estado__in=['pendiente', 'confirmada'],
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                ).exists()
                if not hay_reserva:
                    disponibles.append(hab)
            habitaciones_disponibles = disponibles

    return render(request, 'index.html', {
        'tipos_habitacion': tipos_habitacion,
        'habitaciones_disponibles': habitaciones_disponibles
    })

def consultar_disponibilidad(request):
    disponibles = []
    if request.method == 'POST':
        fecha_entrada = request.POST['fecha_entrada']
        fecha_salida = request.POST['fecha_salida']
        tipo_id = request.POST['tipo_habitacion']

        # Convierte fechas a objetos date
        fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d').date()

        habitaciones = Habitacion.objects.filter(tipo_id=tipo_id)

        for hab in habitaciones:
            hay_reserva = Reserva.objects.filter(
                habitacion=hab,
                estado__in=['pendiente', 'confirmada'],
                fecha_entrada__lt=fecha_salida,
                fecha_salida__gt=fecha_entrada
            ).exists()
            if not hay_reserva:
                disponibles.append(hab)
    return render(request, 'reserva/disponibilidad.html', {'habitaciones': disponibles})

@staff_member_required
def lista_reserva(request):
    reservas = Reserva.objects.all()
    form = ReservaForm()
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reserva')

    return render(request, 'reserva/lista_reserva.html', {
        'reservas': reservas,
        'form': form,
        'accion': 'Agregar',
        'editando': False
    })
@staff_member_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('lista_reserva')
    else:
        form = ReservaForm(instance=reserva)

    reservas = Reserva.objects.all()
    return render(request, 'reserva/lista_reserva.html', {
        'reservas': reservas,
        'form': form,
        'accion': 'Editar',
        'editando': True
    })
@staff_member_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return redirect('lista_reserva')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

