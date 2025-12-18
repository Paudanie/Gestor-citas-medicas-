from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

    # --- PÁGINAS PRINCIPALES ---
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('cambiar_password/', views.cambiar_password, name='cambiar_password'),
    path('reservas/', views.reservas, name='reservas'),
    path('datos_personales/', views.datos_personales, name='datos_personales'),
    path('portal_pacientes/', views.portal_pacientes, name='portal_pacientes'),
    path('portal_doctores/', views.portal_doctores, name='portal_doctores'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path("editar-perfil/", views.editar_perfil, name="editar_perfil"),


    path('test/', views.test, name='test'),

    # ======================================================
    # ==================== USUARIOS ========================
    # ======================================================
    path('lista_doctores/', views.lista_doctores, name='lista_doctores'),


    # =================== PACIENTES ========================
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path("pacientes/<str:rut>/", views.detalle_paciente, name="detalle_paciente"),


    # =================== DOCTORES =========================
    path('doctores/crear/', views.crear_doctor, name='crear_doctor'),
    path('doctores/editar/<int:id>/', views.editar_doctor, name='editar_doctor'),
    path('doctores/eliminar/<int:id>/', views.eliminar_doctor, name='eliminar_doctor'),
    path('lista_pacientes/', views.lista_pacientes, name='lista_pacientes'),

    # ======================================================
    # =================== CITAS MÉDICAS ====================
    # ======================================================
    #path('test/', views.listar_citas, name='listar_citas'),
    #path('citas/', views.listar_citas, name='listar_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('citas/editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
    path('guardar-solicitud/', views.guardar_solicitud_cita, name='guardar_solicitud'),
    path("citas/<str:cita_id>/cancelar/", views.cancelar_cita, name="cancelar_cita"),

    path('citas/<str:cita_id>/confirmar/', views.confirmar_cita, name='confirmar_cita'),
    path('citas/<str:cita_id>/finalizar/', views.finalizar_cita, name='finalizar_cita'),

    path("cita/<str:id_cita>/cancelar/", views.cancelar_cita, name="cancelar_cita"),
    path("cita/<str:id_cita>/editar/", views.editar_cita, name="editar_cita"),
    path("cita/<str:id_cita>/eliminar/", views.eliminar_cita, name="eliminar_cita"),



    # ================= SOLICITUDES ========================
    path('solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),    

    # ======================================================
    # =================== RECETAS ==========================
    # ======================================================
    path('recetas/', views.listar_recetas, name='listar_recetas'),
    #path('recetas/crear/', views.crear_receta, name='crear_receta'),
    path('recetas/editar/<int:id>/', views.editar_receta, name='editar_receta'),
    path('recetas/eliminar/<int:id>/', views.eliminar_receta, name='eliminar_receta'),
    path('recetas/crear/<str:id_cita>/', views.crear_receta_desde_cita, name='crear_receta_desde_cita'),

]





