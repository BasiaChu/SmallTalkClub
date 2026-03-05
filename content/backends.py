from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Jeśli wpisany tekst zawiera małpę '@', szukamy po e-mailu
            if '@' in username:
                user = User.objects.get(email=username)
            # Jeśli nie, szukamy klasycznie po nazwie użytkownika
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        # Jeśli użytkownik istnieje, sprawdzamy, czy hasło pasuje
        if user.check_password(password):
            return user
        return None