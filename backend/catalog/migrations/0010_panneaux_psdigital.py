"""Ajoute les panneaux d'images (catalogue) en tête de la page PS Digital d'un site déjà installé."""
from pathlib import Path

from django.core.files import File
from django.db import migrations
from django.db.models import F

IMAGES = Path(__file__).resolve().parents[1] / "seed" / "images"


def ajouter(apps, schema_editor):
    from catalog.seed import contenu

    Entreprise = apps.get_model("catalog", "Entreprise")
    Section = apps.get_model("catalog", "Section")
    Element = apps.get_model("catalog", "ElementSection")
    e = Entreprise.objects.filter(slug="psdigital").first()
    if not e or Section.objects.filter(entreprise=e, type="panneaux").exists():
        return
    Section.objects.filter(entreprise=e).update(ordre=F("ordre") + 1)
    data = dict(contenu.DIGITAL_PANNEAUX)
    elements = data.pop("elements")
    section = Section.objects.create(page="entreprise", entreprise=e, ordre=0, **data)
    for j, el in enumerate(elements):
        el = dict(el)
        image = el.pop("image")
        element = Element(section=section, ordre=j, **el)
        if image and (IMAGES / image).exists():
            with (IMAGES / image).open("rb") as f:
                element.image.save(Path(image).name, File(f), save=False)
        element.save()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0009_panneaux")]
    operations = [migrations.RunPython(ajouter, migrations.RunPython.noop)]
