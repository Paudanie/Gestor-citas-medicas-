from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class RUTBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        rut = username or kwargs.get("rut")   # Django lo sigue llamando username
        if rut is None or password is None:
            return None

        try:
            user = User.objects.get(rut=rut)
        except User.DoesNotExist:
            return None

        if user.check_password(password):     # importante: hasheada
            return user
        return None
