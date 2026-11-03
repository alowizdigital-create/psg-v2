import pytest
from django.core import mail
from rest_framework.test import APIClient

from demandes.models import Demande
from notifications.models import Notification

URL = "/api/demandes/"


def payload(offre, *options, **extra):
    data = {"offre": offre.slug, "nom": "Jean Mbarga", "telephone": "6 53 83 43 02",
            "email": "jean@example.com", "date_evenement": "2026-12-20", "lieu": "Yaoundé",
            "message": "Mariage de 200 invités", "choix": [o.id for o in options]}
    data.update(extra)
    return data


@pytest.mark.django_db
def test_demande_enregistree_avec_choix_et_total_recalcule(mariage):
    r = APIClient().post(URL, payload(mariage, mariage.o_drone, mariage.o_classique,
                                      total_estime=1, prix=1), format="json")
    assert r.status_code == 201, r.data
    d = Demande.objects.get()
    assert r.data["reference"] == d.reference and d.reference.startswith("PSG-")
    assert d.total_estime == 150000 + 50000  # prix relus en base, jamais ceux du client
    assert [(c.groupe, c.libelle, c.prix) for c in d.choix.all()] == [
        ("Matériel", "Drone", 50000), ("Tenue", "Classique", None)]
    assert d.entreprise == mariage.entreprise and d.offre_titre == "Couverture de mariage"


@pytest.mark.django_db
def test_trois_destinataires_notifies(mariage, superadmin, reglages, gestionnaire_factory, digital,
                                     django_capture_on_commit_callbacks):
    gestionnaire_factory("chef_studio", mariage.entreprise, telephone="690111111")
    gestionnaire_factory("chef_digital", digital, telephone="690222222")
    with django_capture_on_commit_callbacks(execute=True):
        r = APIClient().post(URL, payload(mariage, mariage.o_drone, mariage.o_trad), format="json")
    assert r.status_code == 201
    notifs = Notification.objects.all()
    sms = {(n.type_destinataire, n.destinataire) for n in notifs if n.canal == "sms"}
    assert sms == {
        ("client", "6 53 83 43 02"),
        ("equipe", "699000001"), ("equipe", "690111111"),
        ("superadmin", "677000000"), ("superadmin", "655000000"),
    }  # le gestionnaire de PS Digital n'est pas prévenu
    assert all(n.statut == Notification.ENVOYE for n in notifs)
    client_sms = notifs.get(type_destinataire="client", canal="sms")
    assert "appellera" in client_sms.contenu and d_ref(r) in client_sms.contenu
    destinataires_mail = {m.to[0] for m in mail.outbox}
    assert destinataires_mail == {"jean@example.com", "studio@example.com", "chef_studio@example.com",
                                  "boss@example.com"}
    equipe = next(m for m in mail.outbox if m.to == ["studio@example.com"])
    assert "Drone" in equipe.body and "Traditionnel" in equipe.body and "Jean Mbarga" in equipe.body


def d_ref(r):
    return r.data["reference"]


@pytest.mark.django_db
def test_echec_sms_ne_perd_pas_la_demande(mariage, settings, django_capture_on_commit_callbacks):
    settings.SMS_PROVIDER = "http"
    settings.SMS_HTTP_URL = ""
    with django_capture_on_commit_callbacks(execute=True):
        r = APIClient().post(URL, payload(mariage, mariage.o_classique), format="json")
    assert r.status_code == 201
    d = Demande.objects.get()
    sms = d.notifications.get(canal="sms", type_destinataire="client")
    assert sms.statut == Notification.ECHEC and "SMS_HTTP_URL" in sms.erreur


@pytest.mark.django_db
@pytest.mark.parametrize("choix_attr,erreur", [
    ((), "groupes"),                                   # tenue obligatoire manquante
    (("o_classique", "o_trad"), "groupes"),            # deux choix dans un groupe unique
    (("o_classique", "o_indispo"), "choix"),           # option désactivée
])
def test_regles_des_options(mariage, choix_attr, erreur):
    opts = [getattr(mariage, a) for a in choix_attr]
    r = APIClient().post(URL, payload(mariage, *opts), format="json")
    assert r.status_code == 400 and erreur in r.data
    assert not Demande.objects.exists()


@pytest.mark.django_db
def test_option_d_une_autre_offre_refusee(mariage, studio):
    autre = mariage.__class__.objects.create(entreprise=studio, titre="Shooting", publiee=True)
    from catalog.models import GroupeOptions, Option
    g = GroupeOptions.objects.create(offre=autre, libelle="Fond")
    o = Option.objects.create(groupe=g, libelle="Blanc", prix=1)
    r = APIClient().post(URL, payload(mariage, mariage.o_classique, o), format="json")
    assert r.status_code == 400 and "choix" in r.data


@pytest.mark.django_db
def test_offre_brouillon_refusee(mariage):
    mariage.publiee = False
    mariage.save()
    r = APIClient().post(URL, payload(mariage, mariage.o_classique), format="json")
    assert r.status_code == 400 and "offre" in r.data


@pytest.mark.django_db
def test_telephone_invalide_et_robot(mariage):
    c = APIClient()
    assert "telephone" in c.post(URL, payload(mariage, mariage.o_classique, telephone="12"),
                                 format="json").data
    assert "site_web" in c.post(URL, payload(mariage, mariage.o_classique, site_web="http://spam"),
                                format="json").data
    assert not Demande.objects.exists()


@pytest.mark.django_db
def test_demande_de_contact_sans_offre(studio):
    r = APIClient().post(URL, {"entreprise": studio.slug, "nom": "Awa", "telephone": "+237 690000000",
                               "message": "Bonjour"}, format="json")
    assert r.status_code == 201
    d = Demande.objects.get()
    assert d.entreprise == studio and d.offre is None and d.total_estime is None


@pytest.mark.django_db
def test_limitation_par_ip(mariage, settings):
    from demandes.views import DemandesThrottle
    DemandesThrottle.THROTTLE_RATES = {"demandes": "2/hour"}
    try:
        c = APIClient()
        codes = [c.post(URL, payload(mariage, mariage.o_classique), format="json").status_code
                 for _ in range(3)]
    finally:
        DemandesThrottle.THROTTLE_RATES = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]
    assert codes == [201, 201, 429]
