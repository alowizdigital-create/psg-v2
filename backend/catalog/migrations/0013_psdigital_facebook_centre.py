"""PS Digital : Facebook au centre de la grille des réseaux, panneaux sans bloc de titre."""
from django.db import migrations


def appliquer(apps, schema_editor):
    Section = apps.get_model("catalog", "Section")
    Element = apps.get_model("catalog", "ElementSection")
    for s in Section.objects.filter(entreprise__slug="psdigital", type="losanges"):
        if not s.elements.filter(en_avant=True).exists():
            Element.objects.filter(section=s, titre__iexact="facebook").update(en_avant=True)
    Section.objects.filter(entreprise__slug="psdigital", type="panneaux", titre="Nos services digitaux") \
        .update(sur_titre="", titre="", texte="")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0012_losanges_psdigital")]
    operations = [migrations.RunPython(appliquer, migrations.RunPython.noop)]
