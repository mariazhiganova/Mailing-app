from django.contrib import admin

from mail_flow.models import Recipient, Message, Mailing, MailingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    list_filter = ('full_name', 'email')
    search_fields = ('full_name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'message')
    list_filter = ('start_time', 'status', 'end_time')
    search_fields = ('start_time', 'status', 'end_time')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'status', 'post_response', 'mailing')
    list_filter = ('start_time', 'status', 'post_response',)
    search_fields = ('start_time', 'status', 'post_response',)
