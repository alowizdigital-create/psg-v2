from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Comptes et accès"

    def ready(self):
        from . import signals

        # Relancé après chaque application : la dernière exécution voit toutes les permissions.
        post_migrate.connect(signals.creer_groupe_gestionnaire, dispatch_uid="groupe_gestionnaire")
