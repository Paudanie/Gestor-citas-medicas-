from django.shortcuts import render, redirect
from .models import *
from .forms import *


def inicio(request):
    return render(request, 'gestor/index.html')

def login(request):
    return render(request, 'gestor/login.html')

def reservas(request):
    return render(request, 'gestor/reservar-cita.html')

def PortalPacientes(request):
    return render(request, 'gestor/portal-pacientes.html')



def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # 1️.- Guardar el usuario
            usuario = form.save()

            # 2️.- Crear el perfil según el codigo_seguridad
            codigo = form.cleaned_data.get('codigo_seguridad')
            if codigo == 'codigo_funcionario':
                Funcionario.objects.create(usuario=usuario, rol_trabajo='Recepción')
            elif codigo == 'codigo_doctor':
                Doctor.objects.create(usuario=usuario, especialidad='General')
            else:
                Paciente.objects.create(usuario=usuario)

            # 3️.- Redirigir a la página que quieras
            return redirect('inicio')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
