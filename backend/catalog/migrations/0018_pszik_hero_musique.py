"""PS ZIK : ouverture plein écran « PS ZIK — Production musicale » avec effet musique (une seule fois)."""
from pathlib import Path

from django.core.files import File
from django.db import migrations

IMAGES = Path(__file__).resolve().parents[1] / "seed" / "images"


def appliquer(apps, schema_editor):
    from catalog.seed import contenu

    Entreprise = apps.get_model("catalog", "Entreprise")
    HeroSlide = apps.get_model("catalog", "HeroSlide")
    e = Entreprise.objects.filter(slug="pszik").first()
    if not e:
        return
    if e.hero_style == "photos" and not e.hero_titre:
        e.hero_style, e.hero_titre, e.hero_sous_titre = "musique", "PS ZIK", "Production musicale"
        e.save(update_fields=["hero_style", "hero_titre", "hero_sous_titre"])
    if HeroSlide.objects.filter(entreprise=e).exists():
        return
    for i, (chemin, legende) in enumerate(contenu.SLIDES_ENTREPRISES.get("pszik", [])):
        if not (IMAGES / chemin).exists():
            continue
        slide = HeroSlide(entreprise=e, legende=legende, ordre=i)
        with (IMAGES / chemin).open("rb") as f:
            slide.image.save(Path(chemin).name, File(f), save=False)
        slide.save()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0017_hero_musique")]
    operations = [migrations.RunPython(appliquer, migrations.RunPython.noop)]
