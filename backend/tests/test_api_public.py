import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_offre_publique_cache_options_indisponibles_et_brouillons(mariage, studio):
    from catalog.models import Offre
    Offre.objects.create(entreprise=studio, titre="Brouillon", publiee=False)
    c = APIClient()
    liste = c.get("/api/offres/").json()
    assert [o["titre"] for o in liste] == ["Couverture de mariage"]
    detail = c.get(f"/api/offres/{mariage.slug}/").json()
    libelles = [o["libelle"] for g in detail["groupes"] for o in g["options"]]
    assert "Grue" not in libelles and "Drone" in libelles
    assert c.get("/api/offres/brouillon/").status_code == 404


@pytest.mark.django_db
def test_site_et_pages(studio):
    c = APIClient()
    site = c.get("/api/site/").json()
    assert site["reglages"]["nom"] == "PS GROUP SARL"
    assert [e["slug"] for e in site["entreprises"]] == ["ps-studio-creative"]
    assert c.get("/api/pages/accueil/").status_code == 200
    assert c.get("/api/pages/entreprise/").status_code == 404
    assert c.get(f"/api/entreprises/{studio.slug}/").json()["nom"] == "PS Studio Créative"


@pytest.mark.django_db
def test_diaporama_propre_a_chaque_entreprise(studio):
    import io
    from django.core.files.base import ContentFile
    from PIL import Image
    from catalog.models import HeroSlide

    def img():
        b = io.BytesIO(); Image.new("RGB", (40, 20), "teal").save(b, "PNG")
        return ContentFile(b.getvalue(), name="s.png")

    HeroSlide.objects.create(image=img(), legende="Accueil")
    HeroSlide.objects.create(entreprise=studio, image=img(), legende="Studio")
    HeroSlide.objects.create(entreprise=studio, image=img(), legende="Caché", visible=False)
    c = APIClient()
    assert [s["legende"] for s in c.get("/api/site/").json()["slides"]] == ["Accueil"]
    assert [s["legende"] for s in c.get(f"/api/entreprises/{studio.slug}/").json()["slides"]] == ["Studio"]


@pytest.mark.django_db
def test_seed_page_ps_digital_avec_blocs_animes(settings, tmp_path):
    from django.core.management import call_command
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_contenu", "--sans-offres", verbosity=0)
    page = APIClient().get("/api/entreprises/psdigital/").json()
    types = [s["type"] for s in page["sections"]]
    assert types == ["panneaux", "losanges", "ouverture", "defilant", "survol"]
    ouverture = page["sections"][2]
    assert ouverture["titre"] == "Êtes-vous prêt ?" and [e["titre"] for e in ouverture["elements"]][0] == "Digital"
