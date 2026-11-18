"""Ajoute la grille des réseaux sociaux (losanges) juste avant le bloc « Êtes-vous prêt ? » de PS Digital."""
from django.db import migrations
from django.db.models import F


def ajouter(apps, schema_editor):
    from catalog.seed import contenu

    Entreprise = apps.get_model("catalog", "Entreprise")
    Section = apps.get_model("catalog", "Section")
    Element = apps.get_model("catalog", "ElementSection")
    e = Entreprise.objects.filter(slug="psdigital").first()
    if not e or Section.objects.filter(entreprise=e, type="losanges").exists():
        return
    ouverture = Section.objects.filter(entreprise=e, type="ouverture").order_by("ordre").first()
    if ouverture:
        place = ouverture.ordre
        Section.objects.filter(entreprise=e, ordre__gte=place).update(ordre=F("ordre") + 1)
    else:
        place = (Section.objects.filter(entreprise=e).order_by("-ordre").values_list("ordre", flat=True).first() or 0) + 1
    data = dict(contenu.DIGITAL_LOSANGES)
    elements = data.pop("elements")
    section = Section.objects.create(page="entreprise", entreprise=e, ordre=place, **data)
    for j, el in enumerate(elements):
        el = {k: v for k, v in el.items() if k != "image"}
        Element.objects.create(section=section, ordre=j, **el)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0011_losanges")]
    operations = [migrations.RunPython(ajouter, migrations.RunPython.noop)]
