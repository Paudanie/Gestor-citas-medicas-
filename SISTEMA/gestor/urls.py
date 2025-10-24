from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

    # --- PÁGINAS PRINCIPALES ---
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('reservas/', views.reservas, name='reservas'),
    path('portal_pacientes/', views.portal_pacientes, name='portal_pacientes'),
    path('portal_doctores/', views.portal_doctores, name='portal_doctores'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    path('test/', views.test, name='test'),

    # ======================================================
    # =================== PACIENTES ========================
    # ======================================================
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),

    # ======================================================
    # =================== DOCTORES =========================
    # ======================================================
    path('doctores/', views.listar_doctores, name='listar_doctores'),
    path('doctores/crear/', views.crear_doctor, name='crear_doctor'),
    path('doctores/editar/<int:id>/', views.editar_doctor, name='editar_doctor'),
    path('doctores/eliminar/<int:id>/', views.eliminar_doctor, name='eliminar_doctor'),

    # ======================================================
    # =================== CITAS MÉDICAS ====================
    # ======================================================
    path('citas/', views.listar_citas, name='listar_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('citas/editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
    path('guardar-solicitud/', views.guardar_solicitud_cita, name='guardar_solicitud'),

    # ======================================================
    # =================== RECETAS ==========================
    # ======================================================
    path('recetas/', views.listar_recetas, name='listar_recetas'),
    path('recetas/crear/', views.crear_receta, name='crear_receta'),
    path('recetas/editar/<int:id>/', views.editar_receta, name='editar_receta'),
    path('recetas/eliminar/<int:id>/', views.eliminar_receta, name='eliminar_receta'),
]





