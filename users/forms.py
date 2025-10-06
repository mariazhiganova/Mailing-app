from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from django.forms import TextInput, EmailInput, ModelForm, FileInput

from users.models import CustomUser


class CustomUserCreationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'max-width: 400px;'
            })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль'
        })


class CustomUserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'style': 'max-width: 400px;',
            'placeholder': 'Введите ваш email'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'style': 'max-width: 400px;',
            'placeholder': 'Введите ваш пароль'
        })


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'max-width: 400px;'
            })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'avatar': FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Телефон',
            'avatar': 'Аватар',
        }
