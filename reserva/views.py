from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from habitacion.models import Habitacion
from datetime import datetime
from django.contrib import messages
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
            habitaciones = Habitacion.objects.filter(tipo_id=tipo_id,disponible=True)
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

        habitaciones = Habitacion.objects.filter(tipo_id=tipo_id,disponible=True)

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


@login_required
def mis_reservas(request):
    # No permitir acceso a staff
    if request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Los administradores no pueden ver reservas personales.")

    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        messages.error(request, "Debes completar tu perfil de cliente para ver tus reservas.")
        return redirect('perfil_usuario')
    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'cliente/mis_reservas.html', {'reservas': reservas})


@login_required
def reservar(request):
    cliente = getattr(request.user, 'cliente', None)
    if not cliente or not cliente.perfil_confirmado:
        messages.error(request, "Completa y confirma tu perfil de cliente antes de reservar.")
        return redirect('perfil_usuario')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente
            reserva.save()
            messages.success(request, "Reserva realizada correctamente.")
            return redirect('mis_reservas')
    else:
        form = ReservaForm()

    return render(request, 'reserva/reservar.html', {'form': form})

@login_required
def crear_reserva(request):
    cliente = getattr(request.user, 'cliente', None)
    if not cliente or not cliente.perfil_confirmado:
        messages.error(request, "Debes completar y confirmar tu perfil antes de hacer una reserva.")
        return redirect('perfil_usuario')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente  # Asigna el cliente automáticamente
            reserva.save()
            messages.success(request, "¡Reserva realizada correctamente!")
            return redirect('mis_reservas')
    else:
        form = ReservaForm()

    return render(request, 'reserva/crear_reserva.html', {'form': form})