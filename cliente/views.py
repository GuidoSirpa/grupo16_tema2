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
def perfil_usuario(request):
    user = request.user
    cliente = getattr(user, 'cliente', None)
    if cliente:
        if request.method == 'POST':
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                return redirect('perfil_usuario')  # ← Si quieres, aquí sigue a perfil, o cambia a 'mis_reservas'
        else:
            form = ClienteForm(instance=cliente)
    else:
        if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                nuevo_cliente = form.save(commit=False)
                nuevo_cliente.user = user
                nuevo_cliente.save()
                return redirect('index')  # ← Redirige aquí tras completar perfil
        else:
            form = ClienteForm()
    return render(request, 'cliente/perfil_usuario.html', {'form': form, 'cliente': cliente})
@login_required
def mis_reservas(request):
    # Verifica si el usuario tiene perfil de cliente
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        messages.error(request, "Debes completar tu perfil de cliente para ver tus reservas.")
        return redirect('perfil_usuario')  # o a alguna página para completar el perfil

    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'cliente/mis_reservas.html', {'reservas': reservas})