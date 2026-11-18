"""PS Digital : masque le bloc de tuiles « Développer votre visibilité en ligne » (réactivable dans l'admin)."""
from django.db import migrations


def masquer(apps, schema_editor):
    Section = apps.get_model("catalog", "Section")
    Section.objects.filter(entreprise__slug="psdigital", type="tuiles",
                           titre="Développer votre visibilité en ligne").update(visible=False)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0013_psdigital_facebook_centre")]
    operations = [migrations.RunPython(masquer, migrations.RunPython.noop)]
