from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


# --- FORMULARIOS BÁSICOS ---
class DiscapacidadForm(forms.ModelForm):
    class Meta:
        model = Discapacidad
        fields = '__all__'

class EnfermedadForm(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = '__all__'

class HorarioForm(forms.ModelForm):
    fechaHora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = Horario
        fields = '__all__'

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = '__all__'



# ---- PERSONAS ----
# --- USUARIO ---
class RegistroForm(UserCreationForm):
    codigo_seguridad = forms.CharField(required=False, help_text="Solo para crear funcionarios o doctores")
    # El código de seguridad se ingresa al crear un nuevo usuario. Se ingresa manualmente (ej: "codigo_doctor" o "tu eres el doc", cualquier cosa).
    # Sirve para diferenciar el tipo de usuario que será: paciente(por defcto), doctor o funcionario.
    # De ese modo, un nuevo usuario no puede seleccionar "soy doctor", porque no se sabe el código secreto que hay que ingresar.

    class Meta:
        model = Usuario
        fields = ['rut', 'password1', 'password2', 'fecha_nac', 'telefono', 'direccion', 'discapacidades']
        # rut, password1 y password2 son atributos que debes poner siempre, porque viene en el Auth propio de Django, que es el que estamos usando para la creación de usuarios


# --- PERFILES ---
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['especialidad']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['enfermedades']

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['rol_trabajo']


# --- MODELOS PRINCIPALES ---
class CitaMedicaForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = CitaMedica
        fields = '__all__'

class RecetaForm(forms.ModelForm):
    tratamiento = forms.ModelMultipleChoiceField(
        queryset=Tratamiento.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    fecha_emision = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    vigente_hasta = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Receta
        fields = '__all__'

class HistorialAsistenciaForm(forms.ModelForm):
    class Meta:
        model = HistorialAsistencia
        fields = '__all__'
