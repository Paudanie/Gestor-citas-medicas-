from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError


def crear_notificacion(usuario, mensaje):
    # 1) Guardar notificación interna
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje)

    # 2) Enviar correo
    if usuario.email:
        try:
            send_mail(
                subject="Actualización sobre tu cita médica",
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
                fail_silently=True
            )
        except Exception as e:
            print("❌ Error enviando correo:", e)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import *
from .forms import *
from django.utils.timezone import make_aware
from datetime import datetime, timedelta




# --- PÁGINAS PRINCIPALES ---
def inicio(request):
    doctores = Usuario.objects.all()
    print("Función inicio-llamar doctores, llamada exitosamente.")
    return render(request, 'gestor/index.html', {'doctores': doctores})

def logout_view(request):
    logout(request)
    messages.success(request, "Cierre de sesión exitoso.")
    return redirect('inicio')

def test(request):
    doctores = Usuario.objects.all()
    citas = CitaMedica.objects.all()
    return render(request, 'gestor/test.html', {'doctores': doctores}, {'citas': citas})

def datos_personales(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestor/datos_personales.html', {'usuarios':usuarios})




# Permite logout por GET
LOGOUT_REDIRECT_URL = 'inicio'  # o 'inicio' si tienes nombre de URL


def login_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        print("AUTENTICANDO:", rut, password)  # <--- agrega esto

        user = authenticate(request, rut=rut, password=password)
        print("RESULTADO AUTH:", user)  # <--- agrega esto

        if user is not None:
            auth_login(request, user)
            #print("LOGUEADO OK:", request.user)  # <--- agrega esto
            #print("GRUPOS:", list(request.user.groups.values_list('name', flat=True)))
            messages.success(request, "Inicio de sesión exitoso.")
            if user.groups.filter(name='Doctores').exists():
                return redirect('portal_doctores')

            elif user.groups.filter(name='Pacientes').exists():
                return redirect('portal_pacientes')

            #return redirect('inicio')

        messages.error(request, "Credenciales incorrectas")

    return render(request, 'gestor/login.html')

def reservas(request):
    citas = CitaMedica.objects.all()
    return render(request, 'gestor/reservar-cita.html', {'citas': citas})


'''def portal_pacientes(request):
    citas = CitaMedica.objects.all()
    return render(request,'gestor/portal_pacientes.html', {'citas': citas})
'''

def portal_pacientes(request):

    # 🟢 1. Si está logueado → mostrar sus citas
    if request.user.is_authenticated:
        citas = CitaMedica.objects.filter(paciente=request.user).order_by('fecha_hora')
        return render(request, "gestor/portal_pacientes.html", {
            "usuario_consultado": request.user,
            "citas": citas,
            "modo": "usuario_logueado"
        })

    # 🔵 2. Si NO está logueado, permitir consulta por RUT
    if request.method == "POST":
        rut = request.POST.get("rut")

        try:
            paciente = Usuario.objects.get(rut=rut)
        except Usuario.DoesNotExist:
            messages.error(request, "No existe un paciente con ese RUT.")
            paciente = None
            citas = []
        else:
            citas = CitaMedica.objects.filter(paciente=paciente).order_by('fecha_hora')

        return render(request, "gestor/portal_pacientes.html", {
            "usuario_consultado": paciente,
            "citas": citas,
            "modo": "consulta_rut"
        })

    # 🔸 3. Primera vez visitando → pedir RUT
    return render(request, "gestor/portal_pacientes.html", {
        "modo": "sin_autenticacion"
    })


@login_required
def portal_doctores(request):
    doctores = Usuario.objects.all()
    citas = CitaMedica.objects.all()
    return render(request, 'gestor/portal_doctores.html', {'doctores': doctores, 'citas': citas})

def lista_pacientes(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestor/lista_pacientes.html', {'usuarios':usuarios})

def lista_doctores(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestor/lista_doctores.html', {'usuarios':usuarios})


# --- REGISTRO DE USUARIOS ---
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)

            # Guardar contraseña correctamente
            usuario.set_password(form.cleaned_data['password1'])
            usuario.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login')

    else:
        form = RegistroForm()
    return render(request, 'gestor/registro.html', {'form': form})




@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == "POST":
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Tus datos fueron actualizados.")
            return redirect("portal_pacientes")
    else:
        form = UsuarioUpdateForm(instance=usuario)

    return render(request, "gestor/editar_perfil.html", {"form": form})



# ======================================================
# =================== CRUD PACIENTES ===================
# ======================================================
@login_required
def listar_pacientes(request):
    pacientes = Usuario.objects.all()
    return render(request, 'gestor/pacientes_list.html', {'pacientes': pacientes})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('listar_pacientes')
    else:
        form = UsuarioForm()
    return render(request, 'gestor/paciente_form.html', {'form': form})

@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('listar_pacientes')
    else:
        form = UsuarioForm(instance=paciente)
    return render(request, 'gestor/paciente_form.html', {'form': form})

@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('listar_pacientes')
    return render(request, 'gestor/paciente_confirm_delete.html', {'paciente': paciente})


# ======================================================
# =================== CRUD DOCTORES ====================
# ======================================================
#@login_required
def listar_doctores(request):
    doctores = Usuario.objects.all()
    return render(request, 'gestor/doctores_list.html', {'doctores': doctores})

@login_required
def crear_doctor(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('listar_doctores')
    else:
        form = UsuarioForm()
    return render(request, 'gestor/doctor_form.html', {'form': form})

@login_required
def editar_doctor(request, id):
    doctor = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('listar_doctores')
    else:
        form = UsuarioForm(instance=doctor)
    return render(request, 'gestor/doctor_form.html', {'form': form})

@login_required
def eliminar_doctor(request, id):
    doctor = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('listar_doctores')
    return render(request, 'gestor/doctor_confirm_delete.html', {'doctor': doctor})


# ======================================================
# =================== CRUD CITAS =======================
# ======================================================
#@login_required
def listar_citas(request):
    print("Función listar_citas llamada exitosamente.")
    citas = CitaMedica.objects.all()
    print("Citas encontradas:", citas)
    print("Estoy justo antes del render => citas_list.html")
    return render(request, 'gestor/citas_list.html', {'citas': citas})

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cita creada correctamente.')
                return redirect('listar_citas')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = CitaMedicaForm()
    return render(request, 'gestor/cita_form.html', {'form': form})


@login_required
def editar_cita(request, id_cita):
    cita = get_object_or_404(CitaMedica, id_cita=id_cita)

    # Permisos
    if request.user != cita.paciente and request.user != cita.doctor:
        return HttpResponse("No tienes permiso para editar esta cita.", status=403)

    if request.method == "POST":
        form = CitaEditForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                cita = form.save(commit=False)

                # ---> FIX CLAVE <---
                if cita.estado == "cancelada":
                    cita.estado = "pendiente"

                cita.save()

                messages.success(request, "La cita fue modificada correctamente.")
                return redirect("portal_pacientes")

            except ValidationError as e:
                form.add_error(None, e.message)

    else:
        form = CitaEditForm(instance=cita)

    return render(request, "gestor/editar_cita.html", {"form": form, "cita": cita})



@login_required
def eliminar_cita(request, id_cita):
    cita = get_object_or_404(CitaMedica, id_cita=id_cita)

    # Permisos
    if request.user != cita.paciente and request.user != cita.doctor:
        return HttpResponse("No tienes permiso para eliminar esta cita.", status=403)

    cita.delete()

    messages.success(request, "La cita fue eliminada correctamente.")
    return redirect('portal_pacientes')


def guardar_solicitud_cita(request):
    if request.method == "POST":
        try:
            SolicitudCita.objects.create(
                nombre=request.POST.get("nombre"),
                email=request.POST.get("email"),
                telefono=request.POST.get("telefono"),
                fecha_nac=request.POST.get("fecha_nac"),
                especialidad=request.POST.get("especialidad"),
                doctor_id=request.POST.get("doctor") or None,
                fecha=request.POST.get("fecha"),
                hora=request.POST.get("hora"),
                notas=request.POST.get("notas", "")
            )
            return JsonResponse({"success": True, "message": "Solicitud enviada correctamente."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
    
    return JsonResponse({"success": False, "message": "Método no permitido."})



'''
def confirmar_cita(request, cita_id):
    cita = get_object_or_404(CitaMedica, id_cita=cita_id)

    if request.user != cita.doctor:
        return JsonResponse({"error": "No autorizado"}, status=403)

    fecha_hora = cita.fecha_hora

    # Validación principal
    if not doctor_disponible(cita.doctor, fecha_hora):
        return JsonResponse({
            "ok": False,
            "message": "No puedes confirmar esta cita: está fuera de horario o se cruza con otra."
        })

    cita.estado = "confirmada"
    cita.save()

    return JsonResponse({"ok": True, "message": "Cita confirmada exitosamente."})
'''
@login_required
def confirmar_cita(request, cita_id):
    if request.method != "POST":
        return JsonResponse({"message": "Método no permitido"}, status=405)

    try:
        cita = CitaMedica.objects.get(id_cita=cita_id)
    except CitaMedica.DoesNotExist:
        return JsonResponse({"message": "Cita no encontrada"}, status=404)

    cita.estado = "confirmada"
    cita.save()

    return JsonResponse({"message": "Cita confirmada correctamente"})


@login_required
def finalizar_cita(request, cita_id):
    if request.method != "POST":
        return JsonResponse({"message": "Método no permitido"}, status=405)

    try:
        cita = CitaMedica.objects.get(id_cita=cita_id)
    except CitaMedica.DoesNotExist:
        return JsonResponse({"message": "Cita no encontrada"}, status=404)

    cita.estado = "finalizada"
    cita.save()

    return JsonResponse({"message": "Cita finalizada correctamente"})



@login_required
def cancelar_cita(request, id_cita):
    cita = get_object_or_404(CitaMedica, id_cita=id_cita)

    # Permisos
    if request.user != cita.paciente and request.user != cita.doctor:
        return HttpResponse("No tienes permiso para cancelar esta cita.", status=403)

    cita.estado = "cancelada"
    cita.save()

    messages.success(request, "La cita fue cancelada correctamente.")
    return redirect('portal_pacientes')




def crear_reserva(request):

    # ============================================
    # 1. SI EL USUARIO ESTÁ LOGUEADO → NO PIDE DATOS
    # ============================================
    if request.user.is_authenticated:
        paciente = request.user
        nombre = paciente.first_name
        email = paciente.email
        telefono = paciente.telefono
        fecha_nac = paciente.fecha_nac

    # ============================================
    # 2. SI NO ESTÁ LOGUEADO → FORMULARIO COMPLETO
    # ============================================
    else:
        rut = request.POST.get("rut", "").strip()
        if not rut:
            return JsonResponse({"success": False, "message": "Debe ingresar el RUT"})
        
        email = request.POST.get("email", "").strip()
        if not email:
            return JsonResponse({"success": False, "message": "Debe ingresar el Email"})

        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        fecha_nac = request.POST.get('fecha_nac')

        # Crear o buscar usuario paciente
        paciente, created = Usuario.objects.get_or_create(
            rut=rut,
            defaults={
                'first_name': nombre,
                'email': email,
                'telefono': telefono,
                'fecha_nac': fecha_nac,
                'direccion': 'No especificada',
            }
        )

    # ============================================
    # 3. DATOS DE LA CITA
    # ============================================
    especialidad = request.POST.get('especialidad')
    doctor_rut = request.POST.get('doctor')
    fecha = request.POST.get('fecha')
    hora = request.POST.get('hora')
    notas = request.POST.get('notas')

    # ============================================
    # 4. OBTENER DOCTOR (Usuario del grupo Doctores)
    # ============================================
    if doctor_rut:
        doctor = Usuario.objects.filter(
            rut=doctor_rut,
            groups__name='Doctores'
        ).first()
    else:
        doctor = Usuario.objects.filter(groups__name='Doctores').first()

    if not doctor:
        return JsonResponse({"success": False, "message": "No hay doctores disponibles."})

    # ============================================
    # 5. CONVERTIR fecha + hora A DATETIME REAL
    # ============================================
    try:
        fecha_hora_dt = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        return JsonResponse({"success": False, "message": "Formato de fecha u hora inválido."})

    # ============================================
    # 6. CREAR CITA (con validaciones del modelo)
    # ============================================
    try:
        CitaMedica.objects.create(
            id_cita=f"CITA_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            paciente=paciente,
            doctor=doctor,
            fecha_hora=fecha_hora_dt,
            estado='pendiente',
            notas=notas
        )
    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)})

    messages.success(request, "Tu solicitud de cita fue enviada correctamente.")
    return redirect('portal_pacientes')

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



# SOLICITUDES de citas médicas

def listar_solicitudes(request):
    print("Función listar_solicitudes llamada exitosamente.")
    solicitudes = SolicitudCita.objects.all()
    print("Solicitudes encontradas:", solicitudes)
    return render(request, 'gestor/solicitudes_list.html', {'solicitudes': solicitudes})


def doctor_disponible(doctor, fecha_hora):
    """Devuelve True si el doctor puede tomar la cita."""

    # A) Validar horario laboral
    if doctor.hora_inicio and doctor.hora_fin:
        if not (doctor.hora_inicio <= fecha_hora.time() <= doctor.hora_fin):
            return False

    # B) Validar choque con otras citas
    inicio = fecha_hora
    fin = fecha_hora + timedelta(minutes=30)  # Duración estándar 30 min

    choques = CitaMedica.objects.filter(
        doctor=doctor,
        fecha_hora__lt=fin,
        fecha_hora__gte=inicio - timedelta(minutes=30),
        estado__in=["pendiente", "confirmada"]
    )

    return not choques.exists()
