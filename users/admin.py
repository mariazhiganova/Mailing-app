from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'avatar', 'username', 'first_name', 'last_name', 'is_blocked')
    list_filter = ('email', 'username', 'last_name', 'is_blocked')
    search_fields = ('email', 'username', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Блокировка', {
            'fields': ('is_blocked',),
        }),
    )
