"""PS ZIK : ajoute le bloc « Lecteur de chansons » en tête de page (vide tant qu'aucune chanson n'est ajoutée)."""
from django.db import migrations
from django.db.models import F


def ajouter(apps, schema_editor):
    from catalog.seed import contenu

    Entreprise = apps.get_model("catalog", "Entreprise")
    Section = apps.get_model("catalog", "Section")
    e = Entreprise.objects.filter(slug="pszik").first()
    if not e or Section.objects.filter(entreprise=e, type="musique").exists():
        return
    Section.objects.filter(entreprise=e).update(ordre=F("ordre") + 1)
    data = {k: v for k, v in contenu.ZIK_MUSIQUE.items() if k != "elements"}
    Section.objects.create(page="entreprise", entreprise=e, ordre=0, **data)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0020_lecteur_musique")]
    operations = [migrations.RunPython(ajouter, migrations.RunPython.noop)]
