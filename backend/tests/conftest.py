import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache

from catalog.models import Entreprise, GroupeOptions, Offre, Option, SiteSettings


@pytest.fixture(autouse=True)
def reglages_test(settings, tmp_path):
    settings.NOTIFICATIONS_ASYNC = False
    settings.SMS_PROVIDER = "console"
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.FRONTEND_REVALIDATE_SECRET = ""
    cache.clear()


@pytest.fixture
def studio(db):
    return Entreprise.objects.create(nom="PS Studio Créative", slug="ps-studio-creative",
                                     telephone_equipe="699000001", email_equipe="studio@example.com")


@pytest.fixture
def digital(db):
    return Entreprise.objects.create(nom="PS Digital", slug="ps-digital",
                                     telephone_equipe="699000002", email_equipe="digital@example.com")


@pytest.fixture
def mariage(studio):
    offre = Offre.objects.create(entreprise=studio, titre="Couverture de mariage", publiee=True,
                                 prix_a_partir_de=150000)
    materiel = GroupeOptions.objects.create(offre=offre, libelle="Matériel", type="multiple", ordre=1)
    tenue = GroupeOptions.objects.create(offre=offre, libelle="Tenue", type="unique", obligatoire=True,
                                         ordre=2)
    offre.o_drone = Option.objects.create(groupe=materiel, libelle="Drone", prix=50000)
    offre.o_cadreur = Option.objects.create(groupe=materiel, libelle="Second cadreur", prix=30000)
    offre.o_indispo = Option.objects.create(groupe=materiel, libelle="Grue", prix=90000, disponible=False)
    offre.o_classique = Option.objects.create(groupe=tenue, libelle="Classique")
    offre.o_trad = Option.objects.create(groupe=tenue, libelle="Traditionnel")
    return offre


@pytest.fixture
def superadmin(db):
    u = get_user_model().objects.create_superuser("boss", "boss@example.com", "motdepasse-solide-1")
    u.profil.telephone = "677000000"
    u.profil.save()
    return u


@pytest.fixture
def gestionnaire_factory(db):
    def creer(username, *entreprises, telephone=""):
        u = get_user_model().objects.create_user(username, f"{username}@example.com",
                                                 "motdepasse-solide-1", is_staff=True)
        u.groups.add(Group.objects.get(name="Gestionnaire"))
        u.profil.entreprises.set(entreprises)
        u.profil.telephone = telephone
        u.profil.save()
        return u
    return creer


@pytest.fixture
def reglages(db):
    r = SiteSettings.charger()
    r.supervision_telephones = "655000000"
    r.save()
    return r
