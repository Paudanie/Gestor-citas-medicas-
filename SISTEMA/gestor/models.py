from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


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
    id_usuario = models.CharField(max_length=12, unique=True)
    fecha_nac = models.DateField()
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    discapacidades = models.ManyToManyField(Discapacidad, blank=True) #Ahora, un Usuario puede tener varias Discapacidad dentro del campo "discapacidades", o incluso ninguna

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


class Paciente(Usuario):
    enfermedades = models.ManyToManyField(Enfermedad, blank=True)
#    tratamiento_actual = ¿Le pongo una lista de las recetas que tiene? Es que el doctor ya puede filtrarlas dentro de las mismas recetas, por la id del paciente...
    
    def __str__(self):
        return f"{self.id_usuario} - {self.first_name} {self.last_name}"
    
    def tratamientos_vigentes(self):
        #Devuelve los tratamientos de las recetas aún vigentes
        hoy = date.today()
        return Receta.objects.filter(paciente=self, vigente_hasta__gte=hoy)


class Doctor(Usuario):
    especialidad = models.CharField(max_length=20)
    #    horario_trabajo = models.ManyToManyField(Horario)
    ''' ¿CÓMO HACER EL HORARIO?
    CHATGPT PROPONE COSAS DIFERENTES:
    - CREAR CADA BLOQUE DE HORARIO A TRAVÉS DE UNA NUEVA CLASS QUE TIENE DÍA DE LA SEMANA, HORAINICIO Y HORA FIN, 
    DE FORMA RECURRENTE, TAL VEZ CON UN SCRIPT
    - CREAR UN DATETIME ÚNICO. PARECE QUE ESTO TENDRÍA PROBLEMAS PARA USAR DICHO BLOQUE EN OTRO DOCTOR O CITA MÉDICA
    '''
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.especialidad})"
    
    def citas_pendientes(self):
        #Devuelve las citas pendientes del doctor
        return CitaMedica.objects.filter(doctor=self, estado="pendiente")
  

class Funcionario(Usuario):
    rol_trabajo = models.IntegerField(choices=[
        (0, "Administrador"),
        (1, "Recepcionista"),
        (2, "Call Center"),
        (3, ""),
        (4, ""),
    ])

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_rol_trabajo_display()}"



# -- OTRAS --
class CitaMedica(models.Model):
    id_cita = models.CharField(max_length=20, unique=True)
    paciente = models.ForeignKey("Paciente", on_delete=models.CASCADE)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE)
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
    id_receta = models.CharField(unique=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    cita = models.ForeignKey('CitaMedica', on_delete=models.CASCADE) 
    tratamiento = models.ManyToManyField(Tratamiento)
    indicaciones_extra = models.CharField(max_length=200)
    fecha_emision = models.DateField()
    vigente_hasta = models.DateField()

    def __str__(self):
        return self.nombre


class HistorialAsistencia(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    cita = models.ForeignKey('CitaMedica', on_delete=models.CASCADE) 
    asistencia = models.IntegerField(choices=[
        (0, "Pendiente"),
        (1, "Asistió"),
        (2, "No asistió"),
        # ¿Lo dejamos hasta ahí, o ponemos también las siguientes?
        (3, "Asistió con retraso"),
        (4, "Cancelada por Paciente"),
        (5, "Cancelada por Doctor"),
    ])
    retraso_minutos = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.paciente} - {self.get_asistencia_display()}"







'''
No hace falta esta class si usamos herramientas externas de chatbots de IA, como Rasa o LangChain.
Además, esas herramientas almacenan y organizan los mensajes y conversaciones en otras BDs,
y hasta puedes consultarlas para analizarlas y sacar estadísticas y conclusiones.

class HistorialChatbot(models.Model):
    id_conversacion = models.CharField(unique=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    fechaHora_inicio = models.DateTimeField()
    fechaHora_termino = models.DateTimeField()
    texto_conversacion = models.TextField()
'''