from .models import Usuario

def doctores_context(request):
    doctores = Usuario.objects.exclude(especialidad__isnull=True).exclude(especialidad__exact='')
    return {
        "doctores": doctores
    }
