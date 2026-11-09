from django.contrib import admin

from accounts.admin_mixins import ParEntrepriseMixin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(ParEntrepriseMixin, admin.ModelAdmin):
    chemin_entreprise = "demande__entreprise"
    list_display = ["cree_le", "demande", "type_destinataire", "canal", "destinataire", "statut", "tentatives"]
    list_filter = ["statut", "canal", "type_destinataire"]
    search_fields = ["destinataire", "demande__reference"]
    readonly_fields = [f.name for f in Notification._meta.fields]
    # Journal en lecture seule : aucune action groupée.
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

