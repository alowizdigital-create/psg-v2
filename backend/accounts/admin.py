from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import ProfilGestionnaire
from .permissions import GROUPE_GESTIONNAIRE

User = get_user_model()


class ProfilInline(admin.StackedInline):
    model = ProfilGestionnaire
    can_delete = False
    filter_horizontal = ["entreprises"]
    fields = ["entreprises", "telephone", "recevoir_notifications"]


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfilInline]
    list_display = ["username", "first_name", "last_name", "email", "role", "entreprises_gerees", "is_active"]
    list_filter = ["is_superuser", "is_active", "groups"]

    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "email", "password1", "password2")}),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Identité", {"fields": ("first_name", "last_name", "email")}),
        ("Accès", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups"),
            "description": "Gestionnaire : cocher « Statut équipe », ajouter le groupe « Gestionnaire » "
                           "et choisir ses entreprises plus bas. Superadmin : cocher « Statut "
                           "superutilisateur » (accès total, reçoit toutes les demandes).",
        }),
        ("Dates", {"classes": ("collapse",), "fields": ("last_login", "date_joined")}),
    )

    def get_inline_instances(self, request, obj=None):
        return super().get_inline_instances(request, obj) if obj else []

    def save_model(self, request, obj, form, change):
        if not change and not obj.is_superuser:
            obj.is_staff = True
        super().save_model(request, obj, form, change)
        if not change and not obj.is_superuser:
            groupe = Group.objects.filter(name=GROUPE_GESTIONNAIRE).first()
            if groupe:
                obj.groups.add(groupe)

    @admin.display(description="rôle")
    def role(self, obj):
        return "Superadmin" if obj.is_superuser else "Gestionnaire"

    @admin.display(description="entreprises")
    def entreprises_gerees(self, obj):
        if obj.is_superuser:
            return "Toutes"
        profil = getattr(obj, "profil", None)
        return ", ".join(e.nom for e in profil.entreprises.all()) if profil else "—"

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
