from django.db import models
from django.contrib.auth.models import AbstractUser


# Se crea la clase Discapacidad como un texto varchar
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


class Receta(models.Model):
    id_receta = models.CharField(unique=True)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre

'''
CHATGPT PROPONE QUE HAGAMOS DOS CLASS DIFERENTES:
- CITA MÉDICA: LA CITA CON EL DOCTOR, EN LA AGENDA
- ORDEN MÉDICA: LA ORDEN QUE EMITE EL DOCTOR, PARA EXAMEN, MEDICAMENTO, ETC. 
NO NECESARIAMENTE TODAS LAS CITAS TENDRÁN UNA ORDEN MÉDICA.
PERO CADA ORDEN MÉDICA DEBE HABERSE EMITIDO EN UNA CITA, ¿VERDAD?
'''