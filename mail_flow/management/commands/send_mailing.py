from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from mail_flow.models import Mailing
from mail_flow.services import MailingService


class Command(BaseCommand):
    help = 'Отправляет рассылку по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            MailingService.send_mails(mailing_id)
            self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} отправлена!'))

        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при отправке: {e}'))
