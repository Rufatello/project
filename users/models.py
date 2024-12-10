from django.contrib.auth.models import AbstractUser
from django.db import models
import os

NULLABLE = {
    'blank': True,
    'null': True
}


def avatar_path(instance, name):
    return os.path.join('users_avatar', instance.email, name)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=70, verbose_name='Имя')
    last_name = models.CharField(max_length=70, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to=avatar_path, verbose_name='Аватар')
    surname = models.CharField(max_length=70, verbose_name='Отчество', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

