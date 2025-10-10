from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mail_flow.models import Mailing, MailingAttempt, Recipient


class MailingService:

    @staticmethod
    def send_mails(pk):
        """
        Сервисный метод, который реализует отправку писем всем получателям в рассылке
        """
        mailing = Mailing.objects.get(pk=pk)

        if not mailing.is_active:
            return

        if mailing.status == 'created':
            mailing.status = 'started'
            mailing.start_time = timezone.now()
            mailing.save(update_fields=['status', 'start_time'])

        last_attempt = None

        for recipient in mailing.recipients.all():
            try:
                validate_email(recipient.email)

                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                last_attempt = MailingAttempt.objects.create(
                    mailing=mailing,
                    status='success',
                    post_response='Письма успешно отправлены',
                )

            except ValidationError:
                last_attempt = MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    post_response=f'Невалидный email: {recipient.email}',
                )
            except Exception as e:
                last_attempt = MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    post_response=str(e),
                )

        if mailing.end_time and timezone.now() > mailing.end_time:
            mailing.status = 'completed'
            mailing.save(update_fields=['status'])

        return last_attempt


class StatisticService:
    @staticmethod
    def get_user_statistics(user):
        """
        Получает общую статистику для пользователя с кешированием
        """
        cache_key = f'user_statistics_{user.id}'
        statistics = cache.get(cache_key)

        if statistics is not None:
            return statistics

        total_mailings = Mailing.objects.filter(owner=user).count()
        active_mailings = Mailing.objects.filter(owner=user, status='started').count()
        unique_recipients = Recipient.objects.filter(owner=user).values('email').distinct().count()

        statistics = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
        }

        cache.set(cache_key, statistics, 60 * 15)

        return statistics

    @staticmethod
    def get_mailing_statistics(user):
        """
        Статистика по каждой рассылке отдельно с кешированием
        """
        cache_key = f'mailing_statistics_{user.id}'
        mailings_stats = cache.get(cache_key)

        if mailings_stats is not None:
            return mailings_stats

        mailings = Mailing.objects.filter(owner=user)

        for mailing in mailings:
            mailing.success_count = MailingAttempt.objects.filter(
                mailing=mailing, status='success'
            ).count()
            mailing.failed_count = MailingAttempt.objects.filter(
                mailing=mailing, status='failed'
            ).count()
            mailing.recipients_count = mailing.recipients.count()

        mailings_stats = mailings

        cache.set(cache_key, mailings_stats, 60 * 15)

        return mailings_stats
