from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from reserva.models import Reserva
from .models import Cliente
from .forms import ClienteForm

@staff_member_required
def lista_cliente(request, cliente_id=None):
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        form = ClienteForm(request.POST or None, instance=cliente)
        accion = 'Editar'
    else:
        form = ClienteForm(request.POST or None)
        accion = 'Crear'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('lista_cliente')

    clientes = Cliente.objects.all()
    return render(request, 'cliente/lista_cliente.html', {
        'clientes': clientes,
        'form': form,
        'accion': accion,
        'editando': cliente_id is not None
    })

@staff_member_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_cliente')

@login_required
def mis_reservas(request):
    cliente = getattr(request.user, 'cliente', None)
    if not cliente or not cliente.perfil_confirmado:
        messages.error(request, "Debes completar y confirmar tu perfil antes de ver tus reservas.")
        return redirect('perfil_usuario')
    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'cliente/mis_reservas.html', {'reservas': reservas})

@login_required
def perfil_usuario(request):
    # No permitir acceso a staff
    if request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Los administradores no pueden editar perfil de cliente.")

    user = request.user
    cliente = getattr(user, 'cliente', None)

    if cliente:
        if request.method == 'POST':
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                perfil = form.save(commit=False)
                perfil.perfil_confirmado = True
                perfil.save()
                messages.success(request, "Perfil actualizado y confirmado.")
                return redirect('perfil_usuario')
        else:
            form = ClienteForm(instance=cliente)
    else:
        if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                nuevo_cliente = form.save(commit=False)
                nuevo_cliente.user = user
                nuevo_cliente.perfil_confirmado = True
                nuevo_cliente.save()
                messages.success(request, "Perfil completo. Ya puedes reservar.")
                return redirect('index')
        else:
            form = ClienteForm()
    return render(request, 'cliente/perfil_usuario.html', {'form': form, 'cliente': cliente})