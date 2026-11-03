from django.contrib import admin

from accounts.admin_mixins import ParEntrepriseMixin

from .models import Notification
from .services import relancer


@admin.register(Notification)
class NotificationAdmin(ParEntrepriseMixin, admin.ModelAdmin):
    chemin_entreprise = "demande__entreprise"
    list_display = ["cree_le", "demande", "type_destinataire", "canal", "destinataire", "statut", "tentatives"]
    list_filter = ["statut", "canal", "type_destinataire"]
    search_fields = ["destinataire", "demande__reference"]
    readonly_fields = [f.name for f in Notification._meta.fields]
    actions = ["renvoyer"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description="Renvoyer")
    def renvoyer(self, request, queryset):
        ok = sum(relancer(n).statut == Notification.ENVOYE for n in queryset)
        self.message_user(request, f"{ok}/{queryset.count()} notification(s) envoyée(s).")
