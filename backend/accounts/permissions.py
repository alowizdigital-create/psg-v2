from catalog.models import Entreprise

GROUPE_GESTIONNAIRE = "Gestionnaire"


def entreprises_autorisees(user):
    """Entreprises qu'un utilisateur de l'admin peut gérer."""
    if not user.is_authenticated or not user.is_active:
        return Entreprise.objects.none()
    if user.is_superuser:
        return Entreprise.objects.all()
    return Entreprise.objects.filter(gestionnaires__user=user)


def ids_entreprises_autorisees(user):
    return set(entreprises_autorisees(user).values_list("id", flat=True))
