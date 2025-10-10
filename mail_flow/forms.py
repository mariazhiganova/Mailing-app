from django.forms import ModelForm, CheckboxSelectMultiple, SelectMultiple, DateTimeInput

from mail_flow.models import Recipient, Message, Mailing, MailingAttempt


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Полное имя'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Комментарий'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Предмет письма'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Текст письма'})


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'end_time']
        widgets = {'end_time': DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
                   'recipients': CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите сообщение'})
        self.fields['end_time'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите время окончания'})
