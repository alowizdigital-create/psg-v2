from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import (
    ElementSection,
    Entreprise,
    GroupeOptions,
    HeroSlide,
    Offre,
    OffreImage,
    Option,
    Section,
    SiteSettings,
)
from catalog.seed import contenu

IMAGES = Path(__file__).resolve().parents[2] / "seed" / "images"


def fichier(chemin):
    """Ouvre une image du dossier seed pour l'affecter à un ImageField."""
    f = (IMAGES / chemin).open("rb")
    return File(f, name=Path(chemin).name)


def affecter_image(obj, champ, chemin):
    if chemin:
        with fichier(chemin) as f:
            getattr(obj, champ).save(Path(chemin).name, f, save=False)


class Command(BaseCommand):
    help = "Importe le contenu du premier site (pages, entreprises, équipe, images) et des offres d'exemple."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Supprime d'abord le contenu existant (pas les demandes ni les comptes).")
        parser.add_argument("--sans-offres", action="store_true", help="N'importe pas les offres d'exemple.")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Section.objects.all().delete()
            Offre.objects.all().delete()
            HeroSlide.objects.all().delete()
            Entreprise.objects.all().delete()
        elif Entreprise.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Du contenu existe déjà : rien n'est importé (utilisez --reset pour tout remplacer)."))
            return

        reglages = SiteSettings.charger()
        for champ, valeur in contenu.REGLAGES.items():
            setattr(reglages, champ, valeur)
        reglages.save()

        for i, chemin in enumerate(contenu.SLIDES):
            slide = HeroSlide(ordre=i)
            affecter_image(slide, "image", chemin)
            slide.save()

        for page, sections in contenu.PAGES.items():
            self.creer_sections(sections, page=page)

        entreprises = {}
        for i, data in enumerate(contenu.ENTREPRISES):
            data = dict(data)
            sections = data.pop("sections")
            banniere = data.pop("banniere")
            e = Entreprise(ordre=i, **data)
            affecter_image(e, "banniere", banniere)
            e.save()
            entreprises[e.slug] = e
            self.creer_sections(sections, page=Section.PAGE_ENTREPRISE, entreprise=e)

        if not options["sans_offres"]:
            for i, data in enumerate(contenu.OFFRES):
                self.creer_offre(i, dict(data), entreprises)

        self.stdout.write(self.style.SUCCESS(
            f"{Entreprise.objects.count()} entreprises, {Section.objects.count()} sections, "
            f"{Offre.objects.count()} offres et {HeroSlide.objects.count()} images de diaporama importées."))

    def creer_sections(self, sections, page, entreprise=None):
        for i, data in enumerate(sections):
            data = dict(data)
            elements = data.pop("elements")
            section = Section.objects.create(page=page, entreprise=entreprise, ordre=i, **data)
            for j, el in enumerate(elements):
                el = dict(el)
                image = el.pop("image")
                element = ElementSection(section=section, ordre=j, **el)
                affecter_image(element, "image", image)
                element.save()

    def creer_offre(self, ordre, data, entreprises):
        groupes = data.pop("groupes", [])
        galerie = data.pop("galerie", [])
        image = data.pop("image", "")
        offre = Offre(entreprise=entreprises[data.pop("entreprise")], ordre=ordre, publiee=True, **data)
        affecter_image(offre, "image", image)
        offre.save()
        for k, chemin in enumerate(galerie):
            photo = OffreImage(offre=offre, ordre=k)
            affecter_image(photo, "image", chemin)
            photo.save()
        for k, g in enumerate(groupes):
            g = dict(g)
            opts = g.pop("options")
            groupe = GroupeOptions.objects.create(offre=offre, ordre=k, **g)
            for m, o in enumerate(opts):
                Option.objects.create(groupe=groupe, ordre=m, **o)
