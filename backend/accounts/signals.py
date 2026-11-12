from django.conf import settings
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import ProfilGestionnaire
from .permissions import GROUPE_GESTIONNAIRE

# Droits du groupe « Gestionnaire » : catalogue complet, page de son entreprise,
# consultation et suivi des demandes. Le filtrage par entreprise est fait dans l'admin.
PERMISSIONS_GESTIONNAIRE = {
    "catalog": {
        "offre": ["add", "change", "delete", "view"],
        "groupeoptions": ["add", "change", "delete", "view"],
        "option": ["add", "change", "delete", "view"],
        "offreimage": ["add", "change", "delete", "view"],
        "entreprise": ["change", "view"],
        "section": ["add", "change", "delete", "view"],
        "elementsection": ["add", "change", "delete", "view"],
        "avis": ["add", "change", "delete", "view"],
    },
    "demandes": {"demande": ["change", "view"], "demandechoix": ["view"]},
    "notifications": {"notification": ["view"]},
}


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def creer_profil(sender, instance, created, **kwargs):
    if created:
        ProfilGestionnaire.objects.get_or_create(user=instance)


def creer_groupe_gestionnaire(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    groupe, _ = Group.objects.get_or_create(name=GROUPE_GESTIONNAIRE)
    codenames = [
        (app, f"{action}_{model}")
        for app, modeles in PERMISSIONS_GESTIONNAIRE.items()
        for model, actions in modeles.items()
        for action in actions
    ]
    perms = [
        p for p in Permission.objects.filter(content_type__app_label__in=PERMISSIONS_GESTIONNAIRE)
        if (p.content_type.app_label, p.codename) in codenames
    ]
    groupe.permissions.set(perms)
