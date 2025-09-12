from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.inicio, name='index'),
    path('login/',views.login, name='login'),
    path('reservas/',views.reservas, name='reservas'),
    path('PortalPacientes/',views.PortalPacientes, name='PortalPacientes'),
    path('login/PortalPacientes/', views.PortalPacientes, name='PortalPacientes'),
    path('login/reservas/', views.reservas, name='reservar_cita')
]

