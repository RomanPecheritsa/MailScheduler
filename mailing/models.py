from django.db import models
from mailing.utils import upload_to, NULLABLE


class Client(models.Model):
    """Service client"""

    email = models.EmailField(unique=True, verbose_name="почта")
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(**NULLABLE, verbose_name="комментарий")

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ("full_name",)


class Message(models.Model):
    """Mailing message"""

    title = models.CharField(max_length=100, verbose_name="тема письма")
    body = models.TextField(verbose_name="текст письма")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ("title",)


class Mailing(models.Model):
    """Mailing list"""

    class Status(models.TextChoices):
        CREATED = "CR", "Создана"
        RUNNING = "RN", "Запущена"

    class Frequency(models.TextChoices):
        DAILY = "D", "Раз в день"
        WEEKLY = "W", "Раз в неделю"
        MONTHLY = "M", "Раз в месяц"

    is_active = models.BooleanField(default=True, verbose_name='активность рассылки')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время создания рассылки"
    )
    send_time = models.DateTimeField(
        verbose_name="дата и время первой отправки рассылки"
    )
    frequency = models.CharField(
        max_length=1,
        choices=Frequency.choices,
        default=Frequency.WEEKLY,
        verbose_name="периодичность",
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.PROTECT,
        related_name="mailings",
        verbose_name="сообщения",
    )
    clients = models.ManyToManyField(
        Client, related_name="clients", verbose_name="клиенты"
    )

    def __str__(self):
        return f"Рассылка: {self.id}, Статус: {self.status}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ("-created_at",)


class MailingAttempt(models.Model):
    """Represents an attempt to send a mailing"""

    class Status(models.TextChoices):
        SUCCESS = "SC", "Успешно"
        FAILED = "FL", "Неуспешно"

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="рассылка",
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время попытки отправки"
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, verbose_name="статус попытки"
    )
    server_response = models.TextField(
        verbose_name="ответ почтового сервера", **NULLABLE
    )

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-attempt_time"]
