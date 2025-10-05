from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    first_name = models.fields.CharField(max_length=100, blank=True)
    last_name = models.fields.CharField(max_length=100, blank=True)
    patronymic = models.fields.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    birth_date = models.DateField()
    passport = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.first_name + ' ' + self.last_name
