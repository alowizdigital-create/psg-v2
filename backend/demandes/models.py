from django.db import models
from django.utils import timezone


class Demande(models.Model):
    NOUVELLE = "nouvelle"
    STATUTS = [
        (NOUVELLE, "Nouvelle"),
        ("contactee", "Client contacté"),
        ("confirmee", "Confirmée"),
        ("terminee", "Terminée"),
        ("annulee", "Annulée"),
    ]

    reference = models.CharField("référence", max_length=20, unique=True, blank=True, editable=False)
    offre = models.ForeignKey("catalog.Offre", verbose_name="offre", on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="demandes")
    entreprise = models.ForeignKey("catalog.Entreprise", verbose_name="entreprise",
                                   on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="demandes")
    offre_titre = models.CharField("offre demandée", max_length=160, blank=True,
                                   help_text="Copie du titre au moment de la demande.")
    nom = models.CharField("nom complet", max_length=120)
    telephone = models.CharField("téléphone", max_length=30)
    email = models.EmailField("e-mail", blank=True)
    date_evenement = models.DateField("date de l'événement", null=True, blank=True)
    lieu = models.CharField("lieu", max_length=160, blank=True)
    message = models.TextField("message du client", blank=True)
    total_estime = models.PositiveIntegerField("total estimé (FCFA)", null=True, blank=True)
    statut = models.CharField("statut", max_length=12, choices=STATUTS, default=NOUVELLE, db_index=True)
    notes_internes = models.TextField("notes internes", blank=True,
                                      help_text="Visible uniquement par l'équipe.")
    traitee_par = models.ForeignKey("auth.User", verbose_name="suivie par", on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="demandes_suivies")
    cree_le = models.DateTimeField("reçue le", default=timezone.now, db_index=True)
    modifie_le = models.DateTimeField("modifiée le", auto_now=True)
    ip = models.GenericIPAddressField("adresse IP", null=True, blank=True)

    class Meta:
        verbose_name = "demande client"
        verbose_name_plural = "demandes clients"
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.reference} — {self.nom}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.reference:
            self.reference = f"PSG-{self.cree_le:%Y}-{self.pk:04d}"
            super().save(update_fields=["reference"])

    @property
    def prenom(self):
        return (self.nom or "").split(" ")[0]

    def resume_choix(self):
        """Texte « Groupe : choix, choix » une ligne par groupe."""
        lignes = {}
        for choix in self.choix.all():
            lignes.setdefault(choix.groupe, []).append(choix.libelle)
        return "\n".join(f"{g} : {', '.join(v)}" for g, v in lignes.items())


class DemandeChoix(models.Model):
    """Option cochée par le client, copiée telle qu'elle était au moment de la demande."""

    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="choix")
    option = models.ForeignKey("catalog.Option", on_delete=models.SET_NULL, null=True, blank=True)
    groupe = models.CharField("groupe", max_length=160)
    libelle = models.CharField("choix", max_length=160)
    prix = models.PositiveIntegerField("prix (FCFA)", null=True, blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "choix du client"
        verbose_name_plural = "choix du client"
        ordering = ["ordre", "id"]

    def __str__(self):
        return f"{self.groupe} : {self.libelle}"
