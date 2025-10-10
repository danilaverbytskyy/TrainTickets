from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Client

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Ищем пользователя по email или телефону
            client = Client.objects.get(
                Q(email=username) | Q(phone=username)
            )
            if client.check_password(password):
                return client
        except Client.DoesNotExist:
            return None
        except Client.MultipleObjectsReturned:
            # Если найдено несколько пользователей, берем первого
            clients = Client.objects.filter(
                Q(email=username) | Q(phone=username)
            )
            for client in clients:
                if client.check_password(password):
                    return client
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None