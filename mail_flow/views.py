from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from mail_flow.forms import RecipientForm, MessageForm, MailingForm
from mail_flow.mixsins import NotBlockedMixin, ManagerRestrictedMixin, ManagerOnlyMixin
from mail_flow.models import Recipient, Message, Mailing, MailingAttempt
from mail_flow.services import MailingService, StatisticService
from users.models import CustomUser


class RecipientCreateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mail_flow:recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(NotBlockedMixin, ListView):
    model = Recipient
    template_name = 'recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        cache_key = f'recipients_for_user_{self.request.user.id}'
        recipients = cache.get(cache_key)

        if not recipients:
            if (self.request.user.has_perm('mail_flow.can_view_recipients_list') or
                    self.request.user.groups.filter(name='managers').exists()):
                recipients = Recipient.objects.all()
            else:
                recipients = Recipient.objects.filter(owner=self.request.user)

            cache.set(cache_key, recipients, 60 * 15)

        return recipients


class RecipientUpdateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mail_flow:recipients_list')

    def get_queryset(self):
        if self.request.user.groups.filter(name='managers').exists():
            return Recipient.objects.none()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDeleteView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('mail_flow:recipients_list')

    def get_queryset(self):
        if self.request.user.groups.filter(name='managers').exists():
            return Recipient.objects.none()
        return Recipient.objects.filter(owner=self.request.user)


class MessageCreateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('mail_flow:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageUpdateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('mail_flow:messages_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('mail_flow:messages_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MailingCreateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mail_flow:mailings_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['recipients'].queryset = Recipient.objects.filter(owner=self.request.user)

        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mailing = form.save(commit=False)
        mailing.status = 'created'
        mailing.save()

        form.save_m2m()

        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(NotBlockedMixin, LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        cache_key = f'mailings_for_user_{self.request.user.id}'
        mailings = cache.get(cache_key)

        if not mailings:
            if (self.request.user.has_perm('mail_flow.can_view_mailings_list') or
                    self.request.user.groups.filter(name='Managers').exists()):
                mailings = Mailing.objects.all()
            else:
                mailings = Mailing.objects.filter(owner=self.request.user)

            cache.set(cache_key, mailings, 60 * 15)

        return mailings


class MailingUpdateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('mail_flow:mailings_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['recipients'].queryset = Recipient.objects.filter(owner=self.request.user)

        return form

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mail_flow:mailings_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingAttemptCreateView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        try:
            attempt = MailingService.send_mails(pk)
            messages.success(request, 'Рассылка успешно отправлена!')
            return HttpResponseRedirect(reverse('mail_flow:mailing_attempt_success', kwargs={'pk': attempt.pk}))
        except Exception as e:
            messages.error(request, f'Ошибка при отправке рассылки: {e}')
            return HttpResponseRedirect(reverse('mail_flow:mailing_detail', kwargs={'pk': mailing.pk}))

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingAttemptDetailView(NotBlockedMixin, ManagerRestrictedMixin, LoginRequiredMixin, DetailView):
    model = MailingAttempt
    template_name = 'mailing_attempt_success.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return MailingAttempt.objects.filter(mailing__owner=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingAttemptListView(NotBlockedMixin, LoginRequiredMixin, ListView):
    model = MailingAttempt
    context_object_name = 'mailing_attempt'

    def get_queryset(self):
        cache_key = f'attempts_for_user_{self.request.user.id}'
        attempts = cache.get(cache_key)

        if not attempts:
            attempts = MailingAttempt.objects.filter(mailing__owner=self.request.user)
            cache.set(cache_key, attempts, 60 * 15)

        return attempts

    def get_template_names(self):
        if 'reports' in self.request.path:
            return ['reports.html']
        return ['main.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(StatisticService.get_user_statistics(self.request.user))
        context['mailings_stats'] = StatisticService.get_mailing_statistics(self.request.user)

        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class UsersListView(LoginRequiredMixin, ManagerOnlyMixin, ListView):
    template_name = 'users_list.html'
    model = CustomUser
    context_object_name = 'users'

    def get_queryset(self):
        if not self.request.user.has_perm('users.can_view_users'):
            raise PermissionDenied
        return CustomUser.objects.all()


class BlockUserConfirmView(LoginRequiredMixin, ManagerOnlyMixin, TemplateView):
    template_name = 'block_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['user'] = get_object_or_404(CustomUser, id=pk)
        return context


class BlockUserView(LoginRequiredMixin, ManagerOnlyMixin, View):
    def get(self, request, pk):
        return redirect('mail_flow:block_user_confirm', pk=pk)

    def post(self, request, pk):
        if not request.user.has_perm('users.can_block_user'):
            raise PermissionDenied
        user = get_object_or_404(CustomUser, id=pk)
        user.is_blocked = not user.is_blocked
        user.save()

        return redirect('mail_flow:users_list')


class ToggleMailingView(LoginRequiredMixin, ManagerOnlyMixin, View):
    def post(self, request, pk):
        if not request.user.has_perm('mail_flow.can_disable_mailing'):
            raise PermissionDenied

        mailing = get_object_or_404(Mailing, id=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()

        return redirect('mail_flow:mailings_list')
