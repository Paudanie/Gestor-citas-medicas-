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
    #codigo_seguridad = forms.CharField(required=False)

    class Meta:
        model = Usuario
        fields = [
            'rut',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'fecha_nac',
            'telefono',
            'direccion',
            'discapacidades',
            'enfermedades',
        ]


# --- PERFILES ---
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['especialidad']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['enfermedades']

'''class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        #fields = ['rol_trabajo']
'''


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
