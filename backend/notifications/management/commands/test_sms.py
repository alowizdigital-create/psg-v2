from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from notifications.sms import SmsError, envoyer_sms


class Command(BaseCommand):
    help = "Envoie un SMS de test avec le fournisseur configuré (ex. manage.py test_sms 653834302)."

    def add_arguments(self, parser):
        parser.add_argument("numero")
        parser.add_argument("--message", default="PS GROUP : test d'envoi de SMS depuis le nouveau site.")

    def handle(self, numero, message, **options):
        self.stdout.write(f"Fournisseur : {settings.SMS_PROVIDER} · expéditeur : {settings.SMS_SENDER_ID}")
        try:
            envoyer_sms(numero, message)
        except SmsError as exc:
            raise CommandError(f"Échec : {exc}") from exc
        self.stdout.write(self.style.SUCCESS(f"SMS envoyé à {numero}."))
