"""PS Studio Créative : conversion plus tolérante du bloc « Des images qui marquent » en liste interactive.

La migration 0019 exigeait le titre exact ; celle-ci accepte un titre modifié (majuscules, espaces,
apostrophes) et repère l'entreprise par son adresse ou son nom.
"""
from django.db import migrations
from django.db.models import Q


def appliquer(apps, schema_editor):
    Section = apps.get_model("catalog", "Section")
    entreprise = Q(entreprise__slug="pscreative") | Q(entreprise__nom__icontains="studio")
    bloc = Q(titre__icontains="images qui marquent") | Q(sur_titre__icontains="photographie")
    Section.objects.filter(entreprise, bloc, type="cartes").update(type="survol")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0021_pszik_lecteur")]
    operations = [migrations.RunPython(appliquer, migrations.RunPython.noop)]
