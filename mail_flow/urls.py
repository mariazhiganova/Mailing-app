from django.urls import path

from mail_flow.apps import MailFlowConfig
from mail_flow.views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MailingListView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, MailingAttemptCreateView, MailingAttemptDetailView, MailingAttemptListView, \
    UsersListView, BlockUserView, BlockUserConfirmView, ToggleMailingView

app_name = MailFlowConfig.name

urlpatterns = [
    path('', MailingAttemptListView.as_view(), name='main'),

    path('recipients_list', RecipientListView.as_view(), name='recipients_list'),
    path('recipient/add/', RecipientCreateView.as_view(), name='recipient_form'),
    path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages_list/', MessageListView.as_view(), name='messages_list'),
    path('message/add/', MessageCreateView.as_view(), name='message_form'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings_list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing/add/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('<int:pk>/mailing_attempt/', MailingAttemptCreateView.as_view(), name='mailing_attempt'),
    path('<int:pk>/mailing_attempt/success', MailingAttemptDetailView.as_view(), name='mailing_attempt_success'),

    path('reports/', MailingAttemptListView.as_view(), name='reports'),

    path('users_list/', UsersListView.as_view(), name='users_list'),
    path('user/<int:pk>/block/confirm/', BlockUserConfirmView.as_view(), name='block_user_confirm'),
    path('user/<int:pk>/block/', BlockUserView.as_view(), name='block_user'),

    path('mailing/<int:pk>/toggle/', ToggleMailingView.as_view(), name='toggle_mailing'),
]
