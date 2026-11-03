"""Balises de gabarit de l'interface d'administration (menu latéral, tableau de bord)."""

from datetime import timedelta

from django import template
from django.db.models import Sum
from django.utils import timezone
from django.utils.safestring import mark_safe

from accounts.permissions import entreprises_autorisees
from catalog.admin_icons import ICONES
from catalog.models import Offre
from demandes.models import Demande
from notifications.models import Notification

register = template.Library()

# Icône affichée devant chaque écran dans le menu latéral (clé = nom du modèle).
ICONE_MODELE = {
    "demande": "demande", "offre": "offre", "entreprise": "entreprise", "section": "section",
    "heroslide": "heroslide", "sitesettings": "sitesettings", "notification": "notification",
    "user": "user", "group": "group",
}

# Ordre et intitulés des rubriques du menu.
RUBRIQUES = [
    ("Activité", ["demandes.demande", "notifications.notification"]),
    ("Catalogue", ["catalog.offre", "catalog.entreprise"]),
    ("Site", ["catalog.section", "catalog.heroslide", "catalog.sitesettings"]),
    ("Accès", ["auth.user", "auth.group"]),
]


@register.simple_tag
def icone(nom):
    return mark_safe(ICONES.get(nom, ICONES["default"]))


@register.simple_tag
def rubriques_menu(available_apps):
    """Réorganise la liste des applications de l'admin en rubriques avec icônes."""
    modeles = {}
    for app in available_apps:
        for m in app["models"]:
            modeles[f"{app['app_label']}.{m['object_name'].lower()}"] = m
    resultat, vus = [], set()
    for titre, cles in RUBRIQUES:
        items = []
        for cle in cles:
            if cle in modeles:
                vus.add(cle)
                items.append({**modeles[cle], "icone": ICONE_MODELE.get(cle.split(".")[1], "default")})
        if items:
            resultat.append({"titre": titre, "items": items})
    autres = [{**m, "icone": "default"} for cle, m in modeles.items() if cle not in vus]
    if autres:
        resultat.append({"titre": "Autres", "items": autres})
    return resultat


def _demandes(user):
    qs = Demande.objects.all()
    if not user.is_superuser:
        qs = qs.filter(entreprise__in=entreprises_autorisees(user))
    return qs


@register.simple_tag
def nb_nouvelles_demandes(user):
    if not user.is_authenticated:
        return 0
    return _demandes(user).filter(statut=Demande.NOUVELLE).count()


@register.inclusion_tag("admin/psg_dashboard.html", takes_context=True)
def tableau_de_bord(context):
    user = context["request"].user
    maintenant = timezone.localtime()
    debut_jour = maintenant.replace(hour=0, minute=0, second=0, microsecond=0)
    debut_mois = debut_jour.replace(day=1)
    demandes = _demandes(user)
    du_mois = demandes.filter(cree_le__gte=debut_mois)
    offres = Offre.objects.all() if user.is_superuser else Offre.objects.filter(
        entreprise__in=entreprises_autorisees(user))
    notifications = Notification.objects.filter(demande__in=demandes)

    total_mois = du_mois.aggregate(t=Sum("total_estime"))["t"] or 0
    cartes = [
        {"valeur": demandes.filter(statut=Demande.NOUVELLE).count(), "label": "Demandes à traiter",
         "icone": "demande", "ton": "or", "lien": "/admin/demandes/demande/?statut__exact=nouvelle"},
        {"valeur": demandes.filter(cree_le__gte=debut_jour).count(), "label": "Demandes aujourd'hui",
         "icone": "today", "ton": "bordeaux", "lien": "/admin/demandes/demande/"},
        {"valeur": du_mois.count(), "label": "Demandes ce mois-ci", "icone": "calendar", "ton": "bordeaux",
         "lien": "/admin/demandes/demande/"},
        {"valeur": f"{total_mois:,} XAF".replace(",", " "), "label": "Total estimé du mois",
         "icone": "money", "ton": "bordeaux", "lien": "/admin/demandes/demande/"},
        {"valeur": offres.filter(publiee=True).count(), "label": "Offres publiées", "icone": "offre",
         "ton": "bordeaux", "lien": "/admin/catalog/offre/?publiee__exact=1"},
        {"valeur": offres.filter(publiee=False).count(), "label": "Offres en brouillon", "icone": "section",
         "ton": "gris", "lien": "/admin/catalog/offre/?publiee__exact=0"},
        {"valeur": demandes.filter(statut="contactee").count(), "label": "Clients contactés",
         "icone": "check", "ton": "vert", "lien": "/admin/demandes/demande/?statut__exact=contactee"},
        {"valeur": notifications.filter(statut=Notification.ECHEC).count(), "label": "SMS / e-mails en échec",
         "icone": "alert", "ton": "alerte", "lien": "/admin/notifications/notification/?statut__exact=echec"},
    ]

    # Activité des 14 derniers jours (mini graphique en barres).
    jours = []
    for i in range(13, -1, -1):
        jour = debut_jour - timedelta(days=i)
        jours.append({"date": jour, "n": demandes.filter(cree_le__gte=jour, cree_le__lt=jour + timedelta(days=1)).count()})
    maxi = max([j["n"] for j in jours] + [1])
    for j in jours:
        j["hauteur"] = round(8 + 92 * j["n"] / maxi)

    return {
        "request": context["request"],
        "user": user,
        "aujourdhui": maintenant,
        "cartes": cartes,
        "dernieres": demandes.select_related("entreprise").order_by("-cree_le")[:8],
        "jours": jours,
        "site_url": context.get("site_url"),
    }


@register.filter
def fcfa(montant):
    return f"{montant:,} XAF".replace(",", " ") if montant else "Sur devis"
