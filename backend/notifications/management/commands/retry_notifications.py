from django.core.management.base import BaseCommand

from notifications.models import Notification
from notifications.services import relancer


class Command(BaseCommand):
    help = "Relance l'envoi des notifications (SMS / e-mails) en échec."

    def add_arguments(self, parser):
        parser.add_argument("--max-tentatives", type=int, default=5)

    def handle(self, *args, **options):
        echecs = Notification.objects.filter(
            statut=Notification.ECHEC, tentatives__lt=options["max_tentatives"]
        ).select_related("demande")
        ok = 0
        for n in echecs:
            if relancer(n).statut == Notification.ENVOYE:
                ok += 1
        self.stdout.write(self.style.SUCCESS(f"{ok}/{len(echecs)} notification(s) renvoyée(s)."))
