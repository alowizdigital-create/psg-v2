"""Formation — Class of Week : nouvelle accroche sous le titre de la page."""
from django.db import migrations


def appliquer(apps, schema_editor):
    Entreprise = apps.get_model("catalog", "Entreprise")
    Entreprise.objects.filter(accroche__istartswith="Apprenez les métiers").update(
        accroche="Une formation adaptée pour une insertion plus rapide dans le monde professionnel.")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0023_aide_spotify")]
    operations = [migrations.RunPython(appliquer, migrations.RunPython.noop)]
