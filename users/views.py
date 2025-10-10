from allauth.account.views import SignupView, LoginView as AllauthLoginView, EmailVerificationSentView, \
    PasswordResetView, PasswordResetFromKeyView, PasswordResetDoneView, PasswordResetFromKeyDoneView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView

from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomResetPasswordForm, ProfileForm
from users.models import CustomUser


class RegisterView(SignupView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'


class UserLoginView(AllauthLoginView):
    form_class = CustomUserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('mail_flow:main')


class CustomEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'account/verification_sent.html'


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomResetPasswordForm
    template_name = 'account/password_reset.html'


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'account/password_reset_from_key.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    success_url = 'account/password_reset_from_key_done.html'

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)


class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('users:login'))

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BlockedUserView(TemplateView):
    template_name = 'blocked_page.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile_detail.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'
        return context
