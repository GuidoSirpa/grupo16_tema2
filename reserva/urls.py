from django.urls import path
from . import views



urlpatterns = [
    path('consultar-disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    path('lista_reserva', views.lista_reserva, name='lista_reserva'),
    path('editar_reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('nueva/', views.crear_reserva, name='crear_reserva'),

]
