from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False, default=None)
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокировать', help_text='Заблокирован ли пользователь')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('can_block_user', 'Can block user'),
            ('can_view_users', 'Can view users'),
        ]

    def __str__(self):
        return self.email
