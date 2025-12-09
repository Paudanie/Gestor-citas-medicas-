from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver




# CLASS PREVIAS
class Discapacidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=50)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre
    
class Horario(models.Model):
    fechaHora = models.DateTimeField(unique=True)

    def __str__(self):
        return self.fechaHora
    

class Tratamiento(models.Model):
    medicamento = models.CharField(max_length=50)
    dosis = models.CharField(max_length=20)
    indicaciones = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicamento} {self.dosis}"



# --- CLASS MÁS IMPORTANTES ---
# -- PERSONAS --
class Usuario(AbstractUser): #Al usar AbstractUser, ya tenemos el nombre de usuario, la contraseña, y el manejo seguro de estos
    username = None  # anular campo username por completo
    rut = models.CharField(unique=True, primary_key=True, max_length=12)
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = []  # importantísimo

    fecha_nac = models.DateField()
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    # Solo doctores (opcional)
    especialidad = models.CharField(max_length=50, blank=True, null=True)

    # Solo pacientes (opcional)
    enfermedades = models.ManyToManyField(Enfermedad, blank=True)

    # Si quieres mantener discapacidades
    discapacidades = models.ManyToManyField(Discapacidad, blank=True)

    def __str__(self):
        return f"{self.rut}"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='gestor_usuario_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='gestor_usuario_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            # Si ya viene con password plano, hashearlo
            from django.contrib.auth.hashers import make_password
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


    '''
    def __str__(self):
        return f"{self.rut} - {self.first_name} {self.last_name}"
    '''


@receiver(post_save, sender=Usuario)
def asignar_grupo_paciente(sender, instance, created, **kwargs):
    if created:
        try:
            grupo_pacientes = Group.objects.get(name='Pacientes')
        except Group.DoesNotExist:
            # Si no existe, lo crea automáticamente
            grupo_pacientes = Group.objects.create(name='Pacientes')

        instance.groups.add(grupo_pacientes)



# -- OTRAS --
class CitaMedica(models.Model):
    id_cita = models.CharField(max_length=20, unique=True, primary_key=True)
    #paciente = models.CharField(max_length=12)
    doctor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='citas_como_doctor'
    )

    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='citas_como_paciente'
    )

    fecha_hora = models.DateTimeField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmada", "Confirmada"),
            ("cancelada", "Cancelada"),
            ("finalizada", "Finalizada")
        ],
        default="pendiente"
    )
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita {self.id_cita} - {self.paciente} con {self.doctor} a las {self.fecha_hora}"


class Receta(models.Model):
    id_receta = models.CharField(max_length=20, unique=True)
    doctor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='recetas_emitidas'
    )

    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='recetas_recibidas'
    )

    cita = models.ForeignKey('CitaMedica', on_delete=models.CASCADE)
    tratamiento = models.ManyToManyField(Tratamiento)
    indicaciones_extra = models.CharField(max_length=200)
    fecha_emision = models.DateField()
    vigente_hasta = models.DateField()

    def __str__(self):
        return f"Receta {self.id_receta} - {self.paciente}"



class HistorialAsistencia(models.Model):
    paciente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    cita = models.ForeignKey('CitaMedica', on_delete=models.CASCADE) 
    asistencia = models.IntegerField(choices=[
        (0, "Pendiente"),
        (1, "Asistió"),
        (2, "No asistió"),
        # ¿Lo dejamos hasta ahí, o ponemos también las siguientes?
        (3, "Asistió con retraso"),
        (4, "Cancelada por Usuario"),
        (5, "Cancelada por Usuario"),
    ])
    retraso_minutos = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.paciente} - {self.get_asistencia_display()}"


class SolicitudCita(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_nac = models.DateField()

    especialidad = models.CharField(max_length=50, choices=[
        ('cardiologia', 'Cardiología'),
        ('pediatria', 'Pediatría'),
        ('traumatologia', 'Traumatología'),
        ('neurologia', 'Neurología'),
        ('oftalmologia', 'Oftalmología'),
        ('odontologia', 'Odontología'),
        ('medicina_general', 'Medicina General'),
        ('dermatologia', 'Dermatología'),
    ])

    doctor = models.ForeignKey('Usuario', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'groups__name': 'Doctores'})
    fecha = models.DateField()
    hora = models.TimeField()
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmada", "Confirmada"),
            ("rechazada", "Rechazada")
        ],
        default="pendiente"
    )

    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad} ({self.estado})"

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif. para {self.usuario.rut}: {self.mensaje}"




'''
No hace falta esta class si usamos herramientas externas de chatbots de IA, como Rasa o LangChain.
Además, esas herramientas almacenan y organizan los mensajes y conversaciones en otras BDs,
y hasta puedes consultarlas para analizarlas y sacar estadísticas y conclusiones.

class HistorialChatbot(models.Model):
    id_conversacion = models.CharField(unique=True)
    paciente = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fechaHora_inicio = models.DateTimeField()
    fechaHora_termino = models.DateTimeField()
    texto_conversacion = models.TextField()
'''