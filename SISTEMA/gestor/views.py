from django.shortcuts import render

def inicio(request):
    return render(request, 'gestor/index.html')

def login(request):
    return render(request, 'gestor/login.html')

def reservas(request):
    return render(request, 'gestor/reservar-cita.html')

def PortalPacientes(request):
    return render(request, 'gestor/portal-pacientes.html')