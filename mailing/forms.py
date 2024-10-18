from django import forms
from mailing.models import Client, Message, Mailing, MailingAttempt


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "validate"}),
            "email": forms.EmailInput(attrs={"class": "validate"}),
            "comment": forms.Textarea(attrs={"class": "materialize-textarea"}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input-field"}),
            "body": forms.Textarea(attrs={"class": "materialize-textarea"}),
        }


class MailingForm(forms.ModelForm):
    send_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "validate"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        label="Дата и время первой отправки рассылки",
    )

    class Meta:
        model = Mailing
        fields = [
            "send_time",
            "frequency",
            "message",
            "clients",
        ]
        widgets = {
            "frequency": forms.Select(attrs={"class": "input-field"}),
            "message": forms.Select(attrs={"class": "input-field"}),
            "clients": forms.SelectMultiple(attrs={"class": "input-field"}),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.send_time:
            self.initial["send_time"] = self.instance.send_time.strftime(
                "%Y-%m-%dT%H:%M"
            )
        else:
            self.instance.status = Mailing.Status.CREATED
