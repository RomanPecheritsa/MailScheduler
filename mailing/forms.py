from django import forms

from mailing.models import Client, Message, Mailing
from mailing.mixins import StyleFormMixin as SFM


class ClientForm(SFM, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]


class MessageForm(SFM, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "body"]


class MailingForm(SFM, forms.ModelForm):
    send_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
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

