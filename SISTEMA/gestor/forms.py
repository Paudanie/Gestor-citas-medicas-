from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.conf import settings


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
    codigo_secreto = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Código secreto (solo doctores)'}),
        label="Código de Doctor"
    )

    especialidad = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Especialidad médica'}),
        label="Especialidad"
    )

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
            'especialidad',      # <-- IMPORTANTE: ahora sí existe
        ]

    def clean(self):
        cleaned = super().clean()

        especialidad = cleaned.get("especialidad")
        codigo = cleaned.get("codigo_secreto")

        # Caso 1: Si ingresa especialidad, DEBE ingresar código correcto
        if especialidad:
            if codigo != settings.CODIGO_SECRETO_DOCTOR:
                self.add_error("codigo_secreto", "Código secreto incorrecto.")

        # Caso 2: Si ingresa código pero NO especialidad
        if codigo and not especialidad:
            self.add_error("especialidad", "Debes ingresar una especialidad para registrarte como doctor.")

        return cleaned


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

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "email",
            "telefono",
            "direccion",
            "fecha_nac",
            "discapacidades",
            "enfermedades",
        ]



# --- MODELOS PRINCIPALES ---
class CitaMedicaForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = CitaMedica
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Usuario.objects.exclude(
                especialidad__isnull=True
            ).exclude(
                especialidad=''
            )
        
class CitaEditForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ["doctor", "fecha_hora", "notas"]
        widgets = {
            "fecha_hora": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Usuario.objects.exclude(
                especialidad__isnull=True
            ).exclude(
                especialidad=''
            )
    

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = ['doctor', 'paciente', 'cita', 'id_receta']
        widgets = {

            # 🔹 MULTISELECT TRATAMIENTOS
            'tratamiento': forms.SelectMultiple(
                attrs={
                    'class': (
                        'w-full rounded-lg border border-gray-300 '
                        'focus:border-medical-primary focus:ring-medical-primary '
                        'px-3 py-2'
                    ),
                    'size': 5
                }
            ),

            # 🔹 TEXTAREA CON BORDE VISIBLE
            'indicaciones': forms.Textarea(
                attrs={
                    'class': (
                        'w-full rounded-lg border border-gray-300 '
                        'focus:border-medical-primary focus:ring-medical-primary '
                        'px-3 py-2'
                    ),
                    'rows': 4,
                    'placeholder': 'Indicaciones especiales, precauciones, observaciones...'
                }
            ),

            # 🔹 FECHA (CALENDARIO NATIVO)
            'fecha_emision': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': (
                        'w-full rounded-lg border border-gray-300 '
                        'focus:border-medical-primary focus:ring-medical-primary '
                        'px-3 py-2'
                    )
                }
            ),

            'vigente_hasta': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': (
                        'w-full rounded-lg border border-gray-300 '
                        'focus:border-medical-primary focus:ring-medical-primary '
                        'px-3 py-2'
                    )
                }
            ),
        }

'''
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        exclude = ['doctor', 'paciente', 'cita', 'id_receta']
'''

'''class RecetaForm(forms.ModelForm):
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
'''
class HistorialAsistenciaForm(forms.ModelForm):
    class Meta:
        model = HistorialAsistencia
        fields = '__all__'
