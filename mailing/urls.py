from django.urls import path
from mailing.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ClientDetailView,
    HomePageView,
)
from mailing.apps import MailingConfig

app_name = "mailing"


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/create/", ClientCreateView.as_view(), name="create_client"),
    path("client/edit/<int:pk>/", ClientUpdateView.as_view(), name="edit_client"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="delete_client"),
]
