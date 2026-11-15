from django.core.management.base import BaseCommand

from catalog.management.commands.seed_contenu import ajouter_diaporamas


class Command(BaseCommand):
    help = "Ajoute le diaporama d'ouverture (ex. Miss Afrijeune) aux entreprises qui n'en ont pas. Sans danger si relancée."

    def handle(self, *args, **options):
        n = ajouter_diaporamas()
        self.stdout.write(self.style.SUCCESS(f"{n} image(s) de diaporama ajoutée(s)."))
