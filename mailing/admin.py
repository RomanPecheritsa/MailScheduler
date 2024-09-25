from django.contrib import admin
from mailing.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    ordering = ("id",)
    search_fields = ("email", "full_name")
