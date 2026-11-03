import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html, format_html_join

from accounts.admin_mixins import ParEntrepriseMixin
from notifications.models import Notification
from notifications.services import relancer

from .models import Demande, DemandeChoix


class ChoixInline(admin.TabularInline):
    model = DemandeChoix
    extra = 0
    can_delete = False
    fields = ["groupe", "libelle", "prix_affiche"]
    readonly_fields = fields
    verbose_name_plural = "options cochées par le client"

    @admin.display(description="prix")
    def prix_affiche(self, obj):
        return f"{obj.prix:,} FCFA".replace(",", " ") if obj.prix else "—"

    def has_add_permission(self, request, obj=None):
        return False


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
    can_delete = False
    fields = ["type_destinataire", "canal", "destinataire", "statut", "erreur", "envoye_le"]
    readonly_fields = fields
    verbose_name_plural = "notifications envoyées (client, équipe, superadmin)"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Demande)
class DemandeAdmin(ParEntrepriseMixin, admin.ModelAdmin):
    list_display = ["reference", "cree_le", "nom", "telephone_lien", "offre_titre", "entreprise",
                    "total_affiche", "statut", "notifs"]
    list_display_links = ["reference", "nom"]
    list_editable = ["statut"]
    list_filter = ["statut", "entreprise", ("cree_le", admin.DateFieldListFilter)]
    search_fields = ["reference", "nom", "telephone", "email", "offre_titre", "message"]
    date_hierarchy = "cree_le"
    inlines = [ChoixInline, NotificationInline]
    actions = ["marquer_contactee", "exporter_csv", "renvoyer_notifications"]
    readonly_fields = ["reference", "cree_le", "entreprise", "offre_lien", "offre_titre", "nom",
                       "telephone_lien", "email", "date_evenement", "lieu", "message", "total_affiche",
                       "ip"]
    fieldsets = [
        ("Suivi", {"fields": [("statut", "traitee_par"), "notes_internes"]}),
        ("Demande", {"fields": [("reference", "cree_le"), ("entreprise", "offre_lien"), "total_affiche"]}),
        ("Client", {"fields": [("nom", "telephone_lien"), "email", ("date_evenement", "lieu"), "message"]}),
        ("Technique", {"classes": ["collapse"], "fields": ["ip"]}),
    ]

    def has_add_permission(self, request):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "traitee_par":
            from django.contrib.auth import get_user_model
            kwargs["queryset"] = get_user_model().objects.filter(is_staff=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("entreprise", "offre").prefetch_related(
            "notifications")

    @admin.display(description="téléphone", ordering="telephone")
    def telephone_lien(self, obj):
        chiffres = "".join(c for c in obj.telephone if c.isdigit())
        if len(chiffres) == 9:
            chiffres = "237" + chiffres
        return format_html('<a href="tel:+{}">{}</a> · <a href="https://wa.me/{}" target="_blank">WhatsApp</a>',
                           chiffres, obj.telephone, chiffres)

    @admin.display(description="total estimé", ordering="total_estime")
    def total_affiche(self, obj):
        return f"{obj.total_estime:,} FCFA".replace(",", " ") if obj.total_estime else "sur devis"

    @admin.display(description="offre")
    def offre_lien(self, obj):
        if not obj.offre_id:
            return obj.offre_titre or "Demande de contact"
        return format_html('<a href="/admin/catalog/offre/{}/change/">{}</a>', obj.offre_id, obj.offre_titre)

    @admin.display(description="SMS / e-mails")
    def notifs(self, obj):
        notifs = list(obj.notifications.all())
        if not notifs:
            return "⏳"
        ok = sum(n.statut == Notification.ENVOYE for n in notifs)
        couleur = "#1a7f37" if ok == len(notifs) else "#b42318"
        return format_html('<span style="color:{}">{}/{} envoyés</span>', couleur, ok, len(notifs))

    @admin.action(description="Marquer comme « client contacté »")
    def marquer_contactee(self, request, queryset):
        n = queryset.update(statut="contactee", traitee_par=request.user)
        self.message_user(request, f"{n} demande(s) mise(s) à jour.", messages.SUCCESS)

    @admin.action(description="Renvoyer les notifications en échec")
    def renvoyer_notifications(self, request, queryset):
        echecs = Notification.objects.filter(demande__in=queryset, statut=Notification.ECHEC)
        ok = sum(relancer(n).statut == Notification.ENVOYE for n in echecs)
        self.message_user(request, f"{ok}/{echecs.count() + ok} notification(s) renvoyée(s).")

    @admin.action(description="Exporter en CSV (Excel)")
    def exporter_csv(self, request, queryset):
        reponse = HttpResponse(content_type="text/csv; charset=utf-8")
        reponse["Content-Disposition"] = f'attachment; filename="demandes-{timezone.now():%Y%m%d}.csv"'
        reponse.write("﻿")
        w = csv.writer(reponse, delimiter=";")
        w.writerow(["Référence", "Date", "Entreprise", "Offre", "Nom", "Téléphone", "E-mail",
                    "Date événement", "Lieu", "Choix", "Total estimé", "Statut", "Message"])
        for d in queryset.prefetch_related("choix"):
            w.writerow([d.reference, f"{timezone.localtime(d.cree_le):%d/%m/%Y %H:%M}", d.entreprise or "",
                        d.offre_titre, d.nom, d.telephone, d.email,
                        d.date_evenement.strftime("%d/%m/%Y") if d.date_evenement else "", d.lieu,
                        " | ".join(f"{c.groupe} : {c.libelle}" for c in d.choix.all()),
                        d.total_estime or "", d.get_statut_display(), d.message])
        return reponse
