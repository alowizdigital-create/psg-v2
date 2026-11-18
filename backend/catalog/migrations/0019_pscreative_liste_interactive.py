"""PS Studio Créative : le bloc de cartes « Des images qui marquent » devient une liste interactive."""
from django.db import migrations


def appliquer(apps, schema_editor):
    Section = apps.get_model("catalog", "Section")
    Section.objects.filter(entreprise__slug="pscreative", type="cartes",
                           titre="Des images qui marquent").update(type="survol")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0018_pszik_hero_musique")]
    operations = [migrations.RunPython(appliquer, migrations.RunPython.noop)]
