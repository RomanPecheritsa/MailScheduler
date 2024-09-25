from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)

from mailing.forms import ClientForm
from mailing.models import Client


class HomePageView(TemplateView):
    template_name = "mailing/index.html"


class ClientListView(ListView):
    model = Client
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Клиенты рассылки"
        return context


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
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


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование клиента"
        context["button_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
