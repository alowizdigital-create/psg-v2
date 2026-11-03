from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from .images import ImagesOptimiseesMixin

# Icônes disponibles dans l'admin. La clé est le nom de l'icône Lucide
# utilisée par le site (voir frontend/src/components/Icon.tsx).
ICONES = [
    ("sparkles", "Étincelles"),
    ("clapperboard", "Clap de cinéma"),
    ("camera", "Appareil photo"),
    ("video", "Caméra vidéo"),
    ("film", "Film"),
    ("palette", "Palette"),
    ("hash", "Réseaux sociaux"),
    ("graduation-cap", "Formation"),
    ("music", "Musique"),
    ("mic", "Micro"),
    ("crown", "Couronne"),
    ("satellite-dish", "Média / TV"),
    ("tv", "Télévision"),
    ("wine", "Événement"),
    ("megaphone", "Publicité"),
    ("award", "Récompense"),
    ("target", "Objectif"),
    ("handshake", "Partenariat"),
    ("users", "Équipe"),
    ("badge-check", "Validation"),
    ("code", "Développement web"),
    ("chart-column", "Infographie / statistiques"),
    ("server", "Hébergement"),
    ("ghost", "Snapchat"),
    ("box", "Modélisation 3D"),
    ("list-checks", "Liste / critères"),
    ("square-pen", "Inscription"),
    ("gift", "Cadeau"),
    ("file-signature", "Contrat"),
    ("hotel", "Hôtel"),
    ("map-pin", "Lieu"),
    ("calendar", "Date"),
    ("building-2", "Entreprise"),
    ("layers", "Plusieurs branches"),
    ("workflow", "Processus"),
    ("circle-check", "Réussite"),
    ("heart", "Cœur"),
    ("star", "Étoile"),
    ("plane", "Drone"),
    ("shirt", "Tenue"),
    ("clock", "Durée"),
    ("lightbulb", "Éclairage / idée"),
]


class Ordonnable(models.Model):
    ordre = models.PositiveIntegerField("ordre", default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["ordre", "id"]


def slug_unique(instance, valeur, champ="slug"):
    base = slugify(valeur)[:70] or "element"
    slug, n = base, 2
    Model = type(instance)
    while Model.objects.filter(**{champ: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class Entreprise(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"banniere": 1920}

    nom = models.CharField("nom", max_length=120)
    slug = models.SlugField(
        "adresse de la page", max_length=80, unique=True, blank=True,
        help_text="Partie de l'adresse web (ex. « ps-digital »). Laisser vide pour la générer à partir du nom.",
    )
    sur_titre = models.CharField(
        "sur-titre", max_length=120, blank=True,
        help_text="Petit texte au-dessus du titre de la page (ex. « Nos entreprises — PS Digital »).",
    )
    accroche = models.CharField("accroche", max_length=255, blank=True,
                                help_text="Phrase sous le titre de la page de l'entreprise.")
    resume = models.TextField("résumé (carte d'accueil)", blank=True,
                              help_text="Texte court affiché sur la carte de l'entreprise en page d'accueil.")
    icone = models.CharField("icône", max_length=40, choices=ICONES, default="sparkles")
    banniere = models.ImageField("image bannière", upload_to="entreprises/", blank=True)
    cta_titre = models.CharField("titre de l'appel à l'action", max_length=160, blank=True)
    cta_texte = models.CharField("texte de l'appel à l'action", max_length=255, blank=True)
    telephone_equipe = models.CharField(
        "téléphone de l'équipe", max_length=60, blank=True,
        help_text="Reçoit un SMS à chaque nouvelle demande (plusieurs numéros séparés par des virgules).",
    )
    email_equipe = models.CharField(
        "e-mail de l'équipe", max_length=255, blank=True,
        help_text="Reçoit le détail de chaque nouvelle demande (plusieurs adresses séparées par des virgules).",
    )
    active = models.BooleanField("visible sur le site", default=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "entreprise"
        verbose_name_plural = "entreprises"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_unique(self, self.nom)
        super().save(*args, **kwargs)


class Section(Ordonnable):
    """Bloc de contenu d'une page (accueil, à propos, contact ou page d'entreprise)."""

    PAGE_ACCUEIL = "accueil"
    PAGE_A_PROPOS = "a-propos"
    PAGE_CONTACT = "contact"
    PAGE_ENTREPRISE = "entreprise"
    PAGES = [
        (PAGE_ACCUEIL, "Accueil"),
        (PAGE_A_PROPOS, "À propos"),
        (PAGE_CONTACT, "Contact"),
        (PAGE_ENTREPRISE, "Page d'une entreprise"),
    ]

    TYPES = [
        ("entete", "En-tête de page (titre + texte)"),
        ("texte", "Texte (titre + paragraphes)"),
        ("cartes", "Cartes (icône ou image + titre + texte)"),
        ("tuiles", "Tuiles (icône + titre court)"),
        ("lignes", "Lignes alternées (image + texte)"),
        ("galerie", "Galerie photo"),
        ("personnes", "Personnes (photo + nom + rôle)"),
        ("chiffres", "Chiffres clés animés"),
        ("liste", "Encadré liste (icône + texte)"),
        ("video", "Vidéo (YouTube)"),
        ("liens", "Boutons / liens"),
        ("entreprises", "Grille des entreprises du groupe"),
        ("offres", "Offres du catalogue mises en avant"),
        ("cta", "Bandeau d'appel à l'action"),
    ]

    page = models.CharField("page", max_length=20, choices=PAGES, db_index=True)
    entreprise = models.ForeignKey(
        Entreprise, verbose_name="entreprise", on_delete=models.CASCADE,
        null=True, blank=True, related_name="sections",
        help_text="Obligatoire pour une section de page d'entreprise.",
    )
    type = models.CharField("type de bloc", max_length=20, choices=TYPES)
    sur_titre = models.CharField("sur-titre", max_length=160, blank=True)
    titre = models.CharField("titre", max_length=200, blank=True)
    texte = models.TextField("texte", blank=True,
                             help_text="Laisser une ligne vide entre deux paragraphes.")
    titre_encadre = models.CharField(
        "titre de l'encadré", max_length=120, blank=True,
        help_text="Pour un bloc « Texte » : les éléments s'affichent dans un encadré à droite avec ce titre.",
    )
    bouton_label = models.CharField("texte du bouton", max_length=80, blank=True)
    bouton_lien = models.CharField("lien du bouton", max_length=255, blank=True,
                                   help_text="Ex. /contact, /catalogue ou une adresse https://…")
    fond_alterne = models.BooleanField("fond coloré", default=False)
    colonnes = models.PositiveSmallIntegerField("colonnes", default=3,
                                                choices=[(2, "2"), (3, "3"), (4, "4")])
    visible = models.BooleanField("visible", default=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "section de page"
        verbose_name_plural = "sections de pages"

    def __str__(self):
        cible = self.entreprise.nom if self.entreprise_id else self.get_page_display()
        return f"{cible} — {self.titre or self.get_type_display()}"

    def clean(self):
        if self.page == self.PAGE_ENTREPRISE and not self.entreprise_id:
            raise ValidationError({"entreprise": "Choisissez l'entreprise de cette section."})
        if self.page != self.PAGE_ENTREPRISE:
            self.entreprise = None


class ElementSection(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"image": 1600}

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="elements")
    titre = models.CharField("titre / nom / chiffre", max_length=200, blank=True)
    sous_titre = models.CharField("sous-titre / rôle / libellé", max_length=200, blank=True)
    texte = models.TextField("texte", blank=True)
    icone = models.CharField("icône", max_length=40, choices=ICONES, blank=True)
    image = models.ImageField("image", upload_to="sections/", blank=True)
    lien = models.CharField("lien", max_length=255, blank=True)
    en_avant = models.BooleanField("mis en avant", default=False,
                                   help_text="Ex. le dirigeant dans un bloc « Personnes ».")

    class Meta(Ordonnable.Meta):
        verbose_name = "élément"
        verbose_name_plural = "éléments"

    def __str__(self):
        return self.titre or self.sous_titre or f"Élément {self.pk}"


class Offre(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"image": 1920}

    entreprise = models.ForeignKey(Entreprise, verbose_name="entreprise",
                                   on_delete=models.CASCADE, related_name="offres")
    titre = models.CharField("titre", max_length=160)
    slug = models.SlugField("adresse de la page", max_length=90, unique=True, blank=True,
                            help_text="Laisser vide pour la générer à partir du titre.")
    resume = models.CharField("résumé court", max_length=255, blank=True)
    description = models.TextField("description détaillée", blank=True,
                                   help_text="Laisser une ligne vide entre deux paragraphes.")
    image = models.ImageField("image principale", upload_to="offres/", blank=True)
    prix_a_partir_de = models.PositiveIntegerField(
        "prix « à partir de » (FCFA)", null=True, blank=True,
        help_text="Prix de base ajouté au total estimé. Laisser vide si « sur devis ».",
    )
    publiee = models.BooleanField("publiée", default=False,
                                  help_text="Décoché = brouillon, invisible sur le site.")
    mise_en_avant = models.BooleanField("mise en avant sur l'accueil", default=False)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "offre du catalogue"
        verbose_name_plural = "offres du catalogue"

    def __str__(self):
        return f"{self.titre} ({self.entreprise})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_unique(self, self.titre)
        super().save(*args, **kwargs)


class OffreImage(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"image": 1600}

    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name="galerie")
    image = models.ImageField("image", upload_to="offres/galerie/")
    legende = models.CharField("légende", max_length=160, blank=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "photo de la galerie"
        verbose_name_plural = "galerie photo"

    def __str__(self):
        return self.legende or f"Photo {self.pk}"


class GroupeOptions(Ordonnable):
    MULTIPLE = "multiple"
    UNIQUE = "unique"
    TYPES = [
        (MULTIPLE, "Plusieurs choix possibles (cases à cocher)"),
        (UNIQUE, "Un seul choix (boutons radio)"),
    ]

    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name="groupes")
    libelle = models.CharField("question / libellé", max_length=160,
                               help_text="Ex. « Matériel souhaité », « Type de tenue ».")
    aide = models.CharField("aide pour le client", max_length=255, blank=True)
    type = models.CharField("type de choix", max_length=10, choices=TYPES, default=MULTIPLE)
    obligatoire = models.BooleanField("réponse obligatoire", default=False)
    icone = models.CharField("icône", max_length=40, choices=ICONES, blank=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "groupe d'options"
        verbose_name_plural = "groupes d'options (choix proposés au client)"

    def __str__(self):
        return self.libelle


class Option(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"image": 900}

    groupe = models.ForeignKey(GroupeOptions, on_delete=models.CASCADE, related_name="options")
    libelle = models.CharField("libellé", max_length=160)
    description = models.CharField("description", max_length=255, blank=True)
    prix = models.PositiveIntegerField("prix supplémentaire (FCFA)", null=True, blank=True,
                                       help_text="Laisser vide si inclus ou sur devis.")
    image = models.ImageField("photo", upload_to="options/", blank=True)
    disponible = models.BooleanField("disponible", default=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "option"
        verbose_name_plural = "options"

    def __str__(self):
        return self.libelle


class HeroSlide(ImagesOptimiseesMixin, Ordonnable):
    IMAGES_A_OPTIMISER = {"image": 2200}

    image = models.ImageField("image", upload_to="slides/")
    legende = models.CharField("légende (facultative)", max_length=160, blank=True)
    visible = models.BooleanField("visible", default=True)

    class Meta(Ordonnable.Meta):
        verbose_name = "image du diaporama d'accueil"
        verbose_name_plural = "diaporama d'accueil"

    def __str__(self):
        return self.legende or f"Image {self.pk}"


class SiteSettings(models.Model):
    """Réglages généraux du site (une seule ligne)."""

    nom = models.CharField("nom affiché", max_length=120, default="PS GROUP SARL")
    slogan = models.CharField("slogan", max_length=200,
                              default="L'innovation au service de vos ambitions")
    devise_pied = models.CharField("phrase du pied de page", max_length=200,
                                   default="La vision du futur.")
    adresse = models.CharField("adresse", max_length=255, blank=True)
    telephones = models.CharField("téléphones", max_length=120, blank=True,
                                  help_text="Séparés par des virgules.")
    email = models.EmailField("e-mail de contact", blank=True)
    whatsapp = models.CharField("numéro WhatsApp", max_length=30, blank=True,
                                help_text="Format international sans + (ex. 237653834302).")
    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    tiktok = models.URLField("TikTok", blank=True)
    youtube = models.URLField("YouTube", blank=True)
    supervision_telephones = models.CharField(
        "téléphones de supervision", max_length=255, blank=True,
        help_text="Reçoivent en plus un SMS à chaque demande (en plus des superadmins). Séparés par des virgules.",
    )
    supervision_emails = models.CharField(
        "e-mails de supervision", max_length=255, blank=True,
        help_text="Reçoivent en plus le détail de chaque demande. Séparés par des virgules.",
    )
    sms_confirmation_client = models.CharField(
        "SMS de confirmation au client", max_length=320,
        default=("{nom_site} : bonjour {prenom}, votre demande {reference} est bien reçue. "
                 "Un membre de notre équipe vous appellera très bientôt."),
        help_text="Variables disponibles : {nom_site}, {prenom}, {nom}, {reference}, {offre}.",
    )

    class Meta:
        verbose_name = "réglages du site"
        verbose_name_plural = "réglages du site"

    def __str__(self):
        return "Réglages du site"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def charger(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
