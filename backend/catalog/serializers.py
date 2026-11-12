from django.conf import settings
from rest_framework import serializers

from .models import (
    Avis,
    ElementSection,
    Entreprise,
    GroupeOptions,
    HeroSlide,
    Offre,
    OffreImage,
    Option,
    Section,
    SiteSettings,
)


def url_media(fichier):
    """URL d'un fichier média : relative (/media/...) ou absolue si PUBLIC_BACKEND_URL est défini."""
    if not fichier:
        return None
    return f"{settings.PUBLIC_BACKEND_URL}{fichier.url}"


class ImageField(serializers.Field):
    def __init__(self, **kwargs):
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        return url_media(value)


def paragraphes(texte):
    return [p.strip() for p in (texte or "").replace("\r\n", "\n").split("\n\n") if p.strip()]


class ElementSerializer(serializers.ModelSerializer):
    image = ImageField()
    texte = serializers.SerializerMethodField()

    class Meta:
        model = ElementSection
        fields = ["id", "titre", "sous_titre", "texte", "icone", "image", "lien", "en_avant"]

    def get_texte(self, obj):
        return paragraphes(obj.texte)


class SectionSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(many=True, read_only=True)
    texte = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["id", "type", "sur_titre", "titre", "texte", "titre_encadre", "bouton_label", "bouton_lien",
                  "fond_alterne", "colonnes", "elements"]

    def get_texte(self, obj):
        return paragraphes(obj.texte)


class EntrepriseResumeSerializer(serializers.ModelSerializer):
    banniere = ImageField()

    class Meta:
        model = Entreprise
        fields = ["id", "nom", "slug", "resume", "icone", "banniere", "accroche"]


class OffreResumeSerializer(serializers.ModelSerializer):
    image = ImageField()
    entreprise = EntrepriseResumeSerializer(read_only=True)
    nb_options = serializers.SerializerMethodField()

    class Meta:
        model = Offre
        fields = ["id", "titre", "slug", "resume", "image", "prix_a_partir_de", "entreprise",
                  "nb_options", "mise_en_avant"]

    def get_nb_options(self, obj):
        return sum(len([o for o in g.options.all() if o.disponible]) for g in obj.groupes.all())


class OptionSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = Option
        fields = ["id", "libelle", "description", "prix", "image"]


class GroupeSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = GroupeOptions
        fields = ["id", "libelle", "aide", "type", "obligatoire", "icone", "options"]

    def get_options(self, obj):
        return OptionSerializer([o for o in obj.options.all() if o.disponible], many=True).data


class OffreImageSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = OffreImage
        fields = ["id", "image", "legende"]


class OffreDetailSerializer(OffreResumeSerializer):
    galerie = OffreImageSerializer(many=True, read_only=True)
    groupes = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    avis = serializers.SerializerMethodField()

    class Meta(OffreResumeSerializer.Meta):
        fields = OffreResumeSerializer.Meta.fields + ["description", "galerie", "groupes", "avis"]

    def get_avis(self, obj):
        # Avis de cette offre d'abord, puis avis généraux de l'entreprise (sans offre).
        propres = Avis.objects.filter(publie=True, offre=obj)
        generaux = Avis.objects.filter(publie=True, offre__isnull=True, entreprise_id=obj.entreprise_id)
        return resume_avis([*propres, *generaux])

    def get_description(self, obj):
        return paragraphes(obj.description)

    def get_groupes(self, obj):
        groupes = [g for g in obj.groupes.all() if any(o.disponible for o in g.options.all())]
        return GroupeSerializer(groupes, many=True).data


class EntrepriseDetailSerializer(EntrepriseResumeSerializer):
    sections = serializers.SerializerMethodField()
    offres = serializers.SerializerMethodField()

    class Meta(EntrepriseResumeSerializer.Meta):
        fields = EntrepriseResumeSerializer.Meta.fields + [
            "sur_titre", "cta_titre", "cta_texte", "sections", "offres",
        ]

    def get_sections(self, obj):
        return SectionSerializer([s for s in obj.sections.all() if s.visible], many=True).data

    def get_offres(self, obj):
        offres = [o for o in obj.offres.all() if o.publiee]
        return OffreResumeSerializer(offres, many=True).data


class HeroSlideSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = HeroSlide
        fields = ["id", "image", "legende"]


class SiteSettingsSerializer(serializers.ModelSerializer):
    telephones = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = ["nom", "slogan", "devise_pied", "adresse", "telephones", "email", "whatsapp",
                  "facebook", "instagram", "tiktok", "youtube"]

    def get_telephones(self, obj):
        return [t.strip() for t in obj.telephones.split(",") if t.strip()]


class AvisSerializer(serializers.ModelSerializer):
    photo = ImageField()
    offre = serializers.SerializerMethodField()

    class Meta:
        model = Avis
        fields = ["id", "nom", "qualite", "texte", "note", "photo", "date", "offre"]

    def get_offre(self, obj):
        return {"titre": obj.offre.titre, "slug": obj.offre.slug} if obj.offre_id else None


def resume_avis(avis):
    """Liste d'avis + moyenne et nombre, au format attendu par le site."""
    avis = list(avis)
    total = len(avis)
    moyenne = round(sum(a.note for a in avis) / total, 1) if total else 0
    return {"total": total, "moyenne": moyenne, "liste": AvisSerializer(avis, many=True).data}
