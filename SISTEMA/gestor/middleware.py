from django.shortcuts import redirect
from django.urls import reverse

class ForzarCambioPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if getattr(request.user, 'debe_cambiar_password', False):
                if request.path not in [
                    reverse('cambiar_password'),
                    reverse('logout'),
                ]:
                    return redirect('cambiar_password')

        return self.get_response(request)
