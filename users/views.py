import secrets

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import UserAuthenticationForm, UserCreateForm
from users.models import User
from users.utils import send_email_confirm


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_email_confirm(url, user.email)

        messages.success(
            self.request,
            "Ссылка для подтверждения вашего email была отправлена на указанный адрес.",
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    messages.success(
        request, "Ваш email был успешно подтвержден! Теперь вы можете войти в систему."
    )
    return redirect(reverse("users:login"))



