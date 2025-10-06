from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу менеджеров'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Managers')

        permissions = Permission.objects.filter(
            codename__in=[
                'can_view_mailings_list',
                'can_disable_mailing',
                'can_view_recipients_list',
                'can_view_messages_list',
                'can_view_users',
                'can_block_user',
            ]
        )

        group.permissions.add(*permissions)
