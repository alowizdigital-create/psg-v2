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
