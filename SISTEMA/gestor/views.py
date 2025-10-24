from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import *
from .forms import *


# --- PÁGINAS PRINCIPALES ---
def inicio(request):
    return render(request, 'gestor/index.html')

# Permite logout por GET
LOGOUT_REDIRECT_URL = 'inicio'  # o 'inicio' si tienes nombre de URL


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            
            # Redirigir según el grupo o tipo de usuario
            if user.groups.filter(name='Doctores').exists():
                return redirect('portal_doctores')  # debe coincidir con name en urls.py
            elif user.groups.filter(name='Pacientes').exists():
                return redirect('portal_pacientes')
            else:
                return redirect('inicio')  # fallback si no pertenece a ningún grupo
        else:
            messages.error(request, "Credenciales incorrectas")
            return render(request, 'gestor/login.html')

    return render(request, 'gestor/login.html')

def reservas(request):
    return render(request, 'gestor/reservar-cita.html')

def portal_pacientes(request):
    return render(request, 'gestor/portal_pacientes.html')

def portal_doctores(request):
    return render(request, 'gestor/portal_doctores.html')


# --- REGISTRO DE USUARIOS ---
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            codigo = form.cleaned_data.get('codigo_seguridad')

            # Crear perfil según el código
            if codigo == 'codigo_funcionario':
                Funcionario.objects.create(usuario=usuario, rol_trabajo=1)
            elif codigo == 'codigo_doctor':
                Doctor.objects.create(usuario=usuario, especialidad='General')
            else:
                Paciente.objects.create(usuario=usuario)

            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'gestor/registro.html', {'form': form})


# ======================================================
# =================== CRUD PACIENTES ===================
# ======================================================
@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'gestor/pacientes_list.html', {'pacientes': pacientes})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado correctamente.')
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'gestor/paciente_form.html', {'form': form})

@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'gestor/paciente_form.html', {'form': form})

@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado correctamente.')
        return redirect('listar_pacientes')
    return render(request, 'gestor/paciente_confirm_delete.html', {'paciente': paciente})


# ======================================================
# =================== CRUD DOCTORES ====================
# ======================================================
@login_required
def listar_doctores(request):
    doctores = Doctor.objects.all()
    return render(request, 'gestor/doctores_list.html', {'doctores': doctores})

@login_required
def crear_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor creado correctamente.')
            return redirect('listar_doctores')
    else:
        form = DoctorForm()
    return render(request, 'gestor/doctor_form.html', {'form': form})

@login_required
def editar_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor actualizado correctamente.')
            return redirect('listar_doctores')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'gestor/doctor_form.html', {'form': form})

@login_required
def eliminar_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor eliminado correctamente.')
        return redirect('listar_doctores')
    return render(request, 'gestor/doctor_confirm_delete.html', {'doctor': doctor})


# ======================================================
# =================== CRUD CITAS =======================
# ======================================================
@login_required
def listar_citas(request):
    citas = CitaMedica.objects.all()
    return render(request, 'gestor/citas_list.html', {'citas': citas})

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita creada correctamente.')
            return redirect('listar_citas')
    else:
        form = CitaMedicaForm()
    return render(request, 'gestor/cita_form.html', {'form': form})

@login_required
def editar_cita(request, id):
    cita = get_object_or_404(CitaMedica, id=id)
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('listar_citas')
    else:
        form = CitaMedicaForm(instance=cita)
    return render(request, 'gestor/cita_form.html', {'form': form})

@login_required
def eliminar_cita(request, id):
    cita = get_object_or_404(CitaMedica, id=id)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada correctamente.')
        return redirect('listar_citas')
    return render(request, 'gestor/cita_confirm_delete.html', {'cita': cita})


# ======================================================
# =================== CRUD RECETAS =====================
# ======================================================
@login_required
def listar_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'gestor/recetas_list.html', {'recetas': recetas})

@login_required
def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta creada correctamente.')
            return redirect('listar_recetas')
    else:
        form = RecetaForm()
    return render(request, 'gestor/receta_form.html', {'form': form})

@login_required
def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta actualizada correctamente.')
            return redirect('listar_recetas')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'gestor/receta_form.html', {'form': form})

@login_required
def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if request.method == 'POST':
        receta.delete()
        messages.success(request, 'Receta eliminada correctamente.')
        return redirect('listar_recetas')
    return render(request, 'gestor/receta_confirm_delete.html', {'receta': receta})
