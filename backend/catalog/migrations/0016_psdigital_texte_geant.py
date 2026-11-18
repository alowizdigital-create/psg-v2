"""PS Digital : ajoute le texte géant « PS DIGITAL » qui défile, en fin de page (à la place de la grille des offres)."""
from django.db import migrations
from django.db.models import Max


def ajouter(apps, schema_editor):
    Entreprise = apps.get_model("catalog", "Entreprise")
    Section = apps.get_model("catalog", "Section")
    e = Entreprise.objects.filter(slug="psdigital").first()
    if not e or Section.objects.filter(entreprise=e, type="texte_geant").exists():
        return
    fin = Section.objects.filter(entreprise=e).aggregate(m=Max("ordre"))["m"] or 0
    Section.objects.create(page="entreprise", entreprise=e, type="texte_geant", titre="PS DIGITAL", ordre=fin + 1)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0015_texte_geant")]
    operations = [migrations.RunPython(ajouter, migrations.RunPython.noop)]
