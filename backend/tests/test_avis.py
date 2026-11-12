import pytest
from django.test import Client
from rest_framework.test import APIClient

from catalog.models import Avis


@pytest.fixture
def avis_exemples(mariage, studio, digital):
    return {
        "offre": Avis.objects.create(nom="Awa", texte="Superbe couverture", note=5, offre=mariage),
        "general": Avis.objects.create(nom="Paul", texte="Équipe pro", note=4, entreprise=studio),
        "autre_entreprise": Avis.objects.create(nom="Jean", texte="Bon site", note=3, entreprise=digital),
        "masque": Avis.objects.create(nom="Spam", texte="Caché", note=1, offre=mariage, publie=False),
        "accueil": Avis.objects.create(nom="Marie", texte="Je recommande", note=5, entreprise=studio,
                                       afficher_accueil=True),
    }


@pytest.mark.django_db
def test_offre_affiche_ses_avis_puis_ceux_de_l_entreprise(mariage, avis_exemples):
    d = APIClient().get(f"/api/offres/{mariage.slug}/").json()["avis"]
    noms = [a["nom"] for a in d["liste"]]
    assert noms[0] == "Awa" and set(noms) == {"Awa", "Paul", "Marie"}  # offre d'abord ; ni masqué ni autre entreprise
    assert d["total"] == 3 and d["moyenne"] == pytest.approx(4.7, abs=0.05)


@pytest.mark.django_db
def test_avis_accueil_uniquement_publies_et_coches(avis_exemples):
    d = APIClient().get("/api/avis/?accueil=1").json()
    assert [a["nom"] for a in d["liste"]] == ["Marie"] and d["total"] == 1
    assert APIClient().get("/api/avis/").json()["total"] == 4  # sans les non publiés


@pytest.mark.django_db
def test_entreprise_deduite_de_l_offre(mariage):
    a = Avis.objects.create(nom="X", texte="ok", offre=mariage)
    assert a.entreprise_id == mariage.entreprise_id


@pytest.mark.django_db
def test_aucun_avis(mariage):
    d = APIClient().get(f"/api/offres/{mariage.slug}/").json()["avis"]
    assert d == {"total": 0, "moyenne": 0, "liste": []}


@pytest.mark.django_db
def test_gestionnaire_ne_voit_que_les_avis_de_son_entreprise(avis_exemples, gestionnaire_factory, studio):
    chef = gestionnaire_factory("chef", studio)
    c = Client()
    c.force_login(chef)
    html = c.get("/admin/catalog/avis/").content.decode()
    assert "Awa" in html and "Paul" in html and "Jean" not in html
    assert c.get("/admin/catalog/avis/add/").status_code == 200


@pytest.mark.django_db
def test_bouton_verifier_redirige_vers_whatsapp_sans_exposer_le_numero(mariage):
    a = Avis.objects.create(nom="Awa Ngono", texte="Super", offre=mariage, whatsapp="6 55 33 47 60",
                            accord_verification=True)
    # Le numéro n'apparaît jamais dans l'API publique.
    d = APIClient().get(f"/api/offres/{mariage.slug}/").json()
    assert d["avis"]["liste"][0]["verifiable"] is True
    assert "655334760" not in str(d) and "whatsapp" not in str(d).lower()
    r = Client().get(f"/api/avis/{a.pk}/verifier/")
    assert r.status_code == 302
    assert r["Location"].startswith("https://wa.me/237655334760?text=")
    assert "Awa" in r["Location"] and "Couverture" in r["Location"] and "confirmer" in r["Location"]
    assert r["Cache-Control"] == "no-store"


@pytest.mark.django_db
@pytest.mark.parametrize("champs", [
    {"whatsapp": "655334760", "accord_verification": False},   # pas d'accord du client
    {"whatsapp": "", "accord_verification": False},            # pas de numéro
    {"whatsapp": "655334760", "accord_verification": True, "publie": False},  # masqué
])
def test_bouton_verifier_refuse_sans_accord_numero_ou_publication(mariage, champs):
    a = Avis.objects.create(nom="Awa", texte="Super", offre=mariage, **champs)
    assert Client().get(f"/api/avis/{a.pk}/verifier/").status_code == 404
    assert Client().post(f"/api/avis/{a.pk}/verifier/").status_code == 404


@pytest.mark.django_db
def test_validation_du_numero_whatsapp(mariage):
    from django.core.exceptions import ValidationError
    with pytest.raises(ValidationError):
        Avis(nom="X", texte="ok", offre=mariage, whatsapp="12").full_clean()
    with pytest.raises(ValidationError):
        Avis(nom="X", texte="ok", offre=mariage, accord_verification=True).full_clean()
