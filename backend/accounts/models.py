from django.conf import settings
from django.db import models


class ProfilGestionnaire(models.Model):
    """Rattache un compte de l'admin aux entreprises qu'il gère."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profil", verbose_name="utilisateur")
    entreprises = models.ManyToManyField(
        "catalog.Entreprise", blank=True, related_name="gestionnaires",
        verbose_name="entreprises gérées",
        help_text="Le gestionnaire ne voit et ne modifie que le catalogue et les demandes de ces entreprises.",
    )
    telephone = models.CharField(
        "téléphone (SMS)", max_length=30, blank=True,
        help_text="Reçoit un SMS à chaque nouvelle demande de ses entreprises "
                  "(ou de toutes les entreprises pour un superadmin).",
    )
    recevoir_notifications = models.BooleanField("recevoir les notifications de demandes", default=True)

    class Meta:
        verbose_name = "profil"
        verbose_name_plural = "profil"

    def __str__(self):
        return f"Profil de {self.user}"
