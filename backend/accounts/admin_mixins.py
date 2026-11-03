"""Restriction des écrans de l'admin aux entreprises d'un gestionnaire."""

from django.core.exceptions import PermissionDenied

from catalog.models import Entreprise

from .permissions import entreprises_autorisees, ids_entreprises_autorisees


class ParEntrepriseMixin:
    """Filtre les listes et formulaires sur les entreprises de l'utilisateur.

    ``chemin_entreprise`` : chemin ORM du modèle vers l'entreprise
    (ex. ``"entreprise"`` ou ``"offre__entreprise"``).
    """

    chemin_entreprise = "entreprise"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(**{f"{self.chemin_entreprise}__in": entreprises_autorisees(request.user)})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.related_model is Entreprise and not request.user.is_superuser:
            kwargs["queryset"] = entreprises_autorisees(request.user)
            kwargs["empty_label"] = None
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _entreprise_id(self, obj):
        if self.chemin_entreprise == "pk":
            return obj.pk
        cible = obj
        for part in self.chemin_entreprise.split("__"):
            cible = getattr(cible, part, None)
            if cible is None:
                return None
        return cible.pk

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            eid = self._entreprise_id(obj)
            if eid is not None and eid not in ids_entreprises_autorisees(request.user):
                raise PermissionDenied("Vous ne gérez pas cette entreprise.")
        super().save_model(request, obj, form, change)
