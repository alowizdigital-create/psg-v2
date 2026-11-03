import nested_admin
from django.contrib import admin, messages
from django.db import transaction
from django.utils.html import format_html

from accounts.admin_mixins import ParEntrepriseMixin
from accounts.permissions import entreprises_autorisees

from .models import (
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
from .revalidation import demander_revalidation


def apercu(image, hauteur=48):
    if not image:
        return "—"
    return format_html('<img src="{}" style="height:{}px;border-radius:6px;object-fit:cover">',
                       image.url, hauteur)


class RevalidationMixin:
    """Demande au site de rafraîchir ses pages après chaque modification."""

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        transaction.on_commit(demander_revalidation)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        transaction.on_commit(demander_revalidation)


# --- Offres du catalogue -------------------------------------------------------

class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 0
    min_num = 1
    sortable_field_name = "ordre"
    fields = ["ordre", "libelle", "description", "prix", "image", "disponible"]
    verbose_name = "option proposée"
    verbose_name_plural = "options proposées (le client coche celles qui l'intéressent)"


class GroupeOptionsInline(nested_admin.NestedStackedInline):
    model = GroupeOptions
    extra = 0
    sortable_field_name = "ordre"
    fields = [("libelle", "type", "obligatoire"), ("aide", "icone"), "ordre"]
    inlines = [OptionInline]


class OffreImageInline(nested_admin.NestedTabularInline):
    model = OffreImage
    extra = 0
    sortable_field_name = "ordre"
    fields = ["ordre", "image", "legende"]


@admin.register(Offre)
class OffreAdmin(RevalidationMixin, ParEntrepriseMixin, nested_admin.NestedModelAdmin):
    list_display = ["miniature", "titre", "entreprise", "prix_affiche", "nb_groupes", "publiee",
                    "mise_en_avant", "modifie_le"]
    list_display_links = ["miniature", "titre"]
    list_editable = ["publiee", "mise_en_avant"]
    list_filter = ["publiee", "entreprise"]
    search_fields = ["titre", "resume", "description"]
    readonly_fields = ["apercu_image"]
    actions = ["dupliquer", "publier", "depublier"]
    inlines = [GroupeOptionsInline, OffreImageInline]
    fieldsets = [
        ("L'offre", {"fields": [("entreprise", "publiee", "mise_en_avant"), "titre", "resume",
                                "description"]}),
        ("Image et prix", {"fields": [("image", "apercu_image"), "prix_a_partir_de"]}),
        ("Avancé", {"classes": ["collapse"], "fields": ["slug", "ordre"]}),
    ]

    @admin.display(description="")
    def miniature(self, obj):
        return apercu(obj.image)

    @admin.display(description="aperçu")
    def apercu_image(self, obj):
        return apercu(obj.image, 120)

    @admin.display(description="prix de base")
    def prix_affiche(self, obj):
        return f"{obj.prix_a_partir_de:,} FCFA".replace(",", " ") if obj.prix_a_partir_de else "sur devis"

    @admin.display(description="groupes d'options")
    def nb_groupes(self, obj):
        return obj.groupes.count()

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if not request.user.is_superuser:
            premiere = entreprises_autorisees(request.user).first()
            if premiere:
                initial.setdefault("entreprise", premiere.pk)
        return initial

    @admin.action(description="Dupliquer les offres sélectionnées (en brouillon)")
    def dupliquer(self, request, queryset):
        for offre in queryset.prefetch_related("groupes__options", "galerie"):
            groupes = list(offre.groupes.all())
            galerie = list(offre.galerie.all())
            offre.pk = offre.id = None
            offre.slug = ""
            offre.titre = f"{offre.titre} (copie)"
            offre.publiee = False
            offre.mise_en_avant = False
            offre._state.adding = True
            offre.save()
            for photo in galerie:
                OffreImage.objects.create(offre=offre, image=photo.image.name, legende=photo.legende,
                                          ordre=photo.ordre)
            for g in groupes:
                options = list(g.options.all())
                g.pk = g.id = None
                g.offre = offre
                g._state.adding = True
                g.save()
                for o in options:
                    o.pk = o.id = None
                    o.groupe = g
                    o._state.adding = True
                    o.save()
        self.message_user(request, "Copie(s) créée(s) en brouillon.", messages.SUCCESS)

    @admin.action(description="Publier sur le site")
    def publier(self, request, queryset):
        queryset.update(publiee=True)
        transaction.on_commit(demander_revalidation)

    @admin.action(description="Retirer du site (brouillon)")
    def depublier(self, request, queryset):
        queryset.update(publiee=False)
        transaction.on_commit(demander_revalidation)


# --- Entreprises et pages -----------------------------------------------------------

class ElementInline(nested_admin.NestedStackedInline):
    model = ElementSection
    extra = 0
    sortable_field_name = "ordre"
    fields = [("titre", "sous_titre"), "texte", ("icone", "image", "lien", "en_avant"), "ordre"]


class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    extra = 0
    sortable_field_name = "ordre"
    fk_name = "entreprise"
    fields = [("type", "visible", "fond_alterne", "colonnes"), ("sur_titre", "titre"), "texte",
              ("titre_encadre", "bouton_label", "bouton_lien"), "ordre"]
    inlines = [ElementInline]
    classes = ["collapse"]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["type"].help_text = ""
        return formset


@admin.register(Entreprise)
class EntrepriseAdmin(RevalidationMixin, ParEntrepriseMixin, nested_admin.NestedModelAdmin):
    chemin_entreprise = "pk"
    list_display = ["miniature", "nom", "slug", "nb_offres", "active", "ordre"]
    list_display_links = ["miniature", "nom"]
    list_editable = ["active", "ordre"]
    readonly_fields = ["apercu"]
    inlines = [SectionInline]
    fieldsets = [
        ("Présentation", {"fields": ["nom", ("sur_titre", "icone"), "accroche", "resume",
                                     ("banniere", "apercu")]}),
        ("Bandeau « Nous contacter » en bas de page", {"fields": ["cta_titre", "cta_texte"]}),
        ("Notifications des demandes", {"fields": ["telephone_equipe", "email_equipe"]}),
        ("Avancé", {"classes": ["collapse"], "fields": ["slug", "active", "ordre"]}),
    ]

    def get_queryset(self, request):
        qs = super(ParEntrepriseMixin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk__in=entreprises_autorisees(request.user))

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(description="")
    def miniature(self, obj):
        return apercu(obj.banniere)

    @admin.display(description="aperçu")
    def apercu(self, obj):
        return apercu(obj.banniere, 120)

    @admin.display(description="offres")
    def nb_offres(self, obj):
        return obj.offres.filter(publiee=True).count()


class ElementSectionPageInline(admin.StackedInline):
    model = ElementSection
    extra = 0
    fields = [("titre", "sous_titre"), "texte", ("icone", "image", "lien", "en_avant"), "ordre"]


@admin.register(Section)
class SectionPageAdmin(RevalidationMixin, admin.ModelAdmin):
    """Sections des pages générales (accueil, à propos, contact) — superadmin."""

    list_display = ["__str__", "page", "type", "ordre", "visible"]
    list_editable = ["ordre", "visible"]
    list_filter = ["page", "type"]
    inlines = [ElementSectionPageInline]
    fields = [("page", "type", "visible"), ("sur_titre", "titre"), "texte",
              ("titre_encadre", "bouton_label", "bouton_lien"), ("fond_alterne", "colonnes", "ordre")]

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(page=Section.PAGE_ENTREPRISE)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "page":
            kwargs["choices"] = [c for c in Section.PAGES if c[0] != Section.PAGE_ENTREPRISE]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(HeroSlide)
class HeroSlideAdmin(RevalidationMixin, admin.ModelAdmin):
    list_display = ["miniature", "legende", "ordre", "visible"]
    list_editable = ["ordre", "visible"]

    @admin.display(description="")
    def miniature(self, obj):
        return apercu(obj.image, 60)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Identité", {"fields": ["nom", "slogan", "devise_pied"]}),
        ("Coordonnées", {"fields": ["adresse", "telephones", "email", "whatsapp"]}),
        ("Réseaux sociaux", {"fields": ["facebook", "instagram", "tiktok", "youtube"]}),
        ("Notifications des demandes", {"fields": ["sms_confirmation_client", "supervision_telephones",
                                                   "supervision_emails"]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        obj = SiteSettings.charger()
        return redirect(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", obj.pk)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        transaction.on_commit(demander_revalidation)
