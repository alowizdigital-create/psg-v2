import pytest
from django.test import Client

from demandes.models import Demande


@pytest.fixture
def demandes(mariage, digital):
    a = Demande.objects.create(entreprise=mariage.entreprise, offre=mariage, nom="Client Studio",
                               telephone="690000001")
    b = Demande.objects.create(entreprise=digital, nom="Client Digital", telephone="690000002")
    return a, b


@pytest.mark.django_db
def test_gestionnaire_ne_voit_que_son_entreprise(demandes, gestionnaire_factory, mariage):
    a, b = demandes
    chef = gestionnaire_factory("chef", mariage.entreprise)
    c = Client()
    c.force_login(chef)
    liste = c.get("/admin/demandes/demande/")
    assert liste.status_code == 200
    assert "Client Studio" in liste.content.decode() and "Client Digital" not in liste.content.decode()
    assert c.get(f"/admin/demandes/demande/{a.pk}/change/").status_code == 200
    assert c.get(f"/admin/demandes/demande/{b.pk}/change/").status_code == 302  # introuvable → redirige
    assert c.get("/admin/auth/user/").status_code == 403
    offres = c.get("/admin/catalog/offre/").content.decode()
    assert "Couverture de mariage" in offres


@pytest.mark.django_db
def test_gestionnaire_peut_creer_une_offre_avec_options(gestionnaire_factory, studio, digital):
    from catalog.models import Offre
    chef = gestionnaire_factory("chef", studio)
    c = Client()
    c.force_login(chef)
    page = c.get("/admin/catalog/offre/add/")
    assert page.status_code == 200
    html = page.content.decode()
    assert "PS Studio Créative" in html and "PS Digital</option>" not in html
    assert Offre.objects.count() == 0


@pytest.mark.django_db
def test_superadmin_voit_tout(demandes, superadmin):
    c = Client()
    c.force_login(superadmin)
    html = c.get("/admin/demandes/demande/").content.decode()
    assert "Client Studio" in html and "Client Digital" in html
    assert c.get("/admin/auth/user/").status_code == 200


@pytest.mark.django_db
def test_admin_exige_une_connexion():
    assert Client().get("/admin/demandes/demande/").status_code == 302
