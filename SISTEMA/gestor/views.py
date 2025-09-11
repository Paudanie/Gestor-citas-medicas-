from django.shortcuts import render

def inicio(request):
    return render(request, 'gestor/index.html')

def login(request):
    return render(request, 'gestor/login.html')
