import json
import secrets

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from mailing.mixins import (
    AuthenticationLoginRequiredMixin as AuthLogin,
    PermissionResponseMixin,
)
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
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token

        user.save()

        regular_user_group, created = Group.objects.get_or_create(name="regular_user")

        user.groups.add(regular_user_group)

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_email_confirm(url, user.email)

        messages.success(
            self.request,
            "Ссылка для подтверждения вашего email была отправлена на указанный адрес.",
        )
        return super().form_valid(form)


class UserListView(AuthLogin, PermissionResponseMixin, ListView):
    model = User
    paginate_by = 6
    ordering = ("-date_joined",)
    permission_required = "users.view_user"

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).order_by("-date_joined")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пользователи платформы"
        return context


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    messages.success(
        request, "Ваш email был успешно подтвержден! Теперь вы можете войти в систему."
    )
    return redirect(reverse("users:login"))


class UserToggleActiveView(AuthLogin, PermissionResponseMixin, View):
    permission_required = "users.block_users"

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = json.loads(request.body)
        user.is_active = data["is_active"]
        user.save()
        return JsonResponse({"success": True})
