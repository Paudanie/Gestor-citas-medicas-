from django.db import models
from django.contrib.auth.models import AbstractUser


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



# CLASS MÁS IMPORTANTES
class Usuario(AbstractUser): #Al usar AbstractUser, ya tenemos el nombre de usuario, la contraseña, y el manejo seguro de estos
    id_usuario = models.CharField(max_length=12, unique=True)
    fecha_nac = models.DateField()
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    discapacidades = models.ManyToManyField(Discapacidad, blank=True) #Ahora, un Usuario puede tener varias Discapacidad dentro del campo "discapacidades", o incluso ninguna

class Paciente(Usuario):
    enfermedades = models.ManyToManyField(Enfermedad, blank=True)
#    tratamiento_actual = ¿Le pongo una lista de las recetas que tiene? Es que el doctor ya puede filtrarlas dentro de las mismas recetas, por la id del paciente...

class Doctor(Usuario):
    especialidad = models.CharField(max_length=20)
#    horario_trabajo = models.ManyToManyField(Horario)
'''
¿CÓMO HACER EL HORARIO?
CHATGPT PROPONE COSAS DIFERENTES:
- CREAR CADA BLOQUE DE HORARIO A TRAVÉS DE UNA NUEVA CLASS QUE TIENE DÍA DE LA SEMANA, HORAINICIO Y HORA FIN, 
DE FORMA RECURRENTE, TAL VEZ CON UN SCRIPT
- CREAR UN DATETIME ÚNICO. PARECE QUE ESTO TENDRÍA PROBLEMAS PARA USAR DICHO BLOQUE EN OTRO DOCTOR O CITA MÉDICA
'''

class Funcionario(Usuario):
    rol_trabajo = models.IntegerField(choices=[
        (0, "Administrador"),
        (1, "Recepcionista"),
        (2, "Call Center"),
        (3, ""),
        (4, ""),
    ])




class Receta(models.Model):
    id_receta = models.CharField(unique=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    tratamiento = models.ManyToManyField(Tratamiento)
    indicaciones_extra = models.CharField(max_length=200)
    fecha_emision = models.DateField()
    vigente_hasta = models.DateField()

    def __str__(self):
        return self.nombre

'''
CHATGPT PROPONE QUE HAGAMOS DOS CLASS DIFERENTES:
- CITA MÉDICA: LA CITA CON EL DOCTOR, EN LA AGENDA
- ORDEN MÉDICA: LA ORDEN QUE EMITE EL DOCTOR, PARA EXAMEN, MEDICAMENTO, ETC. 
NO NECESARIAMENTE TODAS LAS CITAS TENDRÁN UNA ORDEN MÉDICA.
PERO CADA ORDEN MÉDICA DEBE HABERSE EMITIDO EN UNA CITA, ¿VERDAD?
Por ende, OrdenMédica vendría a ser lo que yo hice en Receta, ¿cierto?
'''

class HistorialAsistencia(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    #cita = models.ForeignKey('CitaMedica', on_delete=models.CASCADE) 
    #Aún no sé si separar las Citas, por eso lo comenté.
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

class HistorialChatbot(models.Model):
    id_conversacion = models.CharField(unique=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    fechaHora_inicio = models.DateTimeField()
    fechaHora_termino = models.DateTimeField()
    texto_conversacion = models.TextField()
