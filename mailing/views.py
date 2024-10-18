import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
    View,
)

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt
from mailing.mixins import AuthenticationLoginRequiredMixin as ALRM


class HomePageView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Планировщик Рассылок"
        return context


class ClientListView(ALRM, ListView):
    model = Client
    paginate_by = 6
    ordering = ("-id",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Клиенты рассылки"
        return context


class ClientDetailView(ALRM, DetailView):
    model = Client


class ClientCreateView(ALRM, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить нового клиента"
        context["button_text"] = "Добавить"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientUpdateView(ALRM, UpdateView):
    model = Client
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование клиента"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(ALRM, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")


class MessageListView(ALRM, ListView):
    model = Message
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сообщения рассылки"
        return context


class MessageDetailView(ALRM, DetailView):
    model = Message


class MessageCreateView(ALRM, CreateView):
    model = Message
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новое сообщение для рассылки"
        context["button_text"] = "Добавить"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageUpdateView(ALRM, UpdateView):
    model = Message
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование сообщения"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(ALRM, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(ALRM, ListView):
    model = Mailing
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список рассылок"
        return context


class MailingDetailView(ALRM, DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новую рассылку"
        context["button_text"] = "Добавить"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingUpdateView(ALRM, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование рассылки"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(ALRM, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


class MailingToggleActiveView(ALRM, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        data = json.loads(request.body)
        mailing.is_active = data["is_active"]
        mailing.save()
        return JsonResponse({"success": True})


class MailingAttemptListView(ALRM, ListView):
    model = MailingAttempt
    context_object_name = "messageattempt_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Отчет рассылок"
        return context

    def get_queryset(self):
        return MailingAttempt.objects.select_related("mailing").order_by(
            "-attempt_time"
        )
