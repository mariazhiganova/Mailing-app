from django.db.models import EmailField, Model, CharField, TextField, DateTimeField, ForeignKey, ManyToManyField, \
    CASCADE, BooleanField

from config import settings


class Recipient(Model):
    email = EmailField(verbose_name='Email')
    full_name = CharField(max_length=100, verbose_name='ФИО')
    comment = TextField(max_length=500, null=True, blank=True, verbose_name='Комментарий')
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['full_name']
        unique_together = ['email', 'owner']

        permissions = [
            ('can_view_recipients_list', 'Can view recipients list'),
        ]


class Message(Model):
    subject = CharField(max_length=100, verbose_name='Тема письма')
    body = TextField(verbose_name='Текст письма')
    owner = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['subject']

        permissions = [
            ('can_view_messages_list', 'Can view messages list'),
        ]

    def __str__(self):
        return self.subject


class Mailing(Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = DateTimeField(auto_now_add=True, verbose_name='Время начала рассылки')
    end_time = DateTimeField(null=True, blank=True, verbose_name='Время окончания рассылки')
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    message = ForeignKey(Message, on_delete=CASCADE, verbose_name='Сообщение')
    recipients = ManyToManyField(Recipient, verbose_name='Получатели')
    owner = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=CASCADE, verbose_name='Владелец')
    is_active = BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['start_time', 'status']

        permissions = [
            ('can_view_mailings_list', 'Can view mailings list'),
            ('can_disable_mailing', 'Can disable mailing'),
        ]

    def __str__(self):
        return self.message.subject


class MailingAttempt(Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    start_time = DateTimeField(auto_now_add=True, verbose_name='Время попытки рассылки')
    status = CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    post_response = TextField(verbose_name='Ответ почтового сервера')
    mailing = ForeignKey(Mailing, on_delete=CASCADE, verbose_name='Письмо')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['start_time', 'post_response']

    def __str__(self):
        return f"Попытка рассылки {self.pk}"
