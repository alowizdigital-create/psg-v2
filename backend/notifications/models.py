from django.db import models


class Notification(models.Model):
    SMS = "sms"
    EMAIL = "email"
    CANAUX = [(SMS, "SMS"), (EMAIL, "E-mail")]

    CLIENT = "client"
    EQUIPE = "equipe"
    SUPERADMIN = "superadmin"
    DESTINATAIRES = [(CLIENT, "Client"), (EQUIPE, "Équipe de l'entreprise"), (SUPERADMIN, "Superadmin")]

    EN_ATTENTE = "en_attente"
    ENVOYE = "envoye"
    ECHEC = "echec"
    STATUTS = [(EN_ATTENTE, "⏳ En attente"), (ENVOYE, "✅ Envoyé"), (ECHEC, "⚠️ Échec")]

    demande = models.ForeignKey("demandes.Demande", on_delete=models.CASCADE,
                                related_name="notifications", verbose_name="demande")
    canal = models.CharField("canal", max_length=10, choices=CANAUX)
    type_destinataire = models.CharField("pour", max_length=12, choices=DESTINATAIRES)
    destinataire = models.CharField("destinataire", max_length=255)
    sujet = models.CharField("sujet", max_length=255, blank=True)
    contenu = models.TextField("contenu")
    statut = models.CharField("statut", max_length=12, choices=STATUTS, default=EN_ATTENTE, db_index=True)
    erreur = models.TextField("erreur", blank=True)
    tentatives = models.PositiveSmallIntegerField("tentatives", default=0)
    cree_le = models.DateTimeField("créée le", auto_now_add=True)
    envoye_le = models.DateTimeField("envoyée le", null=True, blank=True)

    class Meta:
        verbose_name = "notification envoyée"
        verbose_name_plural = "journal des notifications"
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.get_canal_display()} → {self.destinataire} ({self.get_statut_display()})"
