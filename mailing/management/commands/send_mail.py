from django.core.management import BaseCommand
from mailing.services.mailing_service import send_mailing
from mailing.models import Mailing


class Command(BaseCommand):
    help = "Send an immediate mailing."

    def handle(self, *args, **options):
        while True:
            mailings = Mailing.objects.filter(status=Mailing.Status.CREATED)

            if not mailings:
                print("Нет доступных рассылок для отправки.")
                return

            print("\nДоступные рассылки:")
            print(
                f"{'Номер рассылки':<15} {'Номер сообщения':<20} {'Количество клиентов':<25}"
            )
            for mailing in mailings:
                print(
                    f"{mailing.id:<15} {mailing.message.id:<20} {mailing.clients.count():<25}"
                )

            print("\nВведите номер рассылки для отправки или 'q' для выхода:")
            user_input = input()

            if user_input.lower() == "q":
                print("Выход из программы.")
                break

            if user_input.isdigit():
                mailing_id = int(user_input)
                if Mailing.objects.filter(pk=mailing_id).exists():
                    mailing = Mailing.objects.get(pk=mailing_id)
                    send_mailing(mailing)
                    print(f"Рассылка {mailing.id} запущена.")
                    break
                else:
                    print("Такой рассылки не существует.")
            else:
                print(
                    "Пожалуйста, введите правильный номер рассылки или 'q' для выхода."
                )
