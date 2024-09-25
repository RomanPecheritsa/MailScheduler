from django import forms
from mailing.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "email", "comment"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "validate"}),
            "email": forms.EmailInput(attrs={"class": "validate"}),
            "comment": forms.Textarea(attrs={"class": "materialize-textarea"}),
        }
