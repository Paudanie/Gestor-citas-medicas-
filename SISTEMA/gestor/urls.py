from django.urls import path, include
from . import views00

urlpatterns = [
    path('',views00.inicio, name='index'),
    path('login/',views00.login, name='login'),
    path('reservas/',views00.reservas, name='reservas'),
    path('PortalPacientes/',views00.PortalPacientes, name='PortalPacientes'),
    path('login/PortalPacientes/', views00.PortalPacientes, name='PortalPacientes'),
    path('login/reservas/', views00.reservas, name='reservar_cita')
]

