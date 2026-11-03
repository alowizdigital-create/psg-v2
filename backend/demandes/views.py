import logging
import threading

from django.conf import settings
from django.db import close_old_connections, transaction
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle

from notifications.services import notifier_nouvelle_demande

from .models import Demande
from .serializers import DemandeCreateSerializer

logger = logging.getLogger(__name__)


class DemandesThrottle(SimpleRateThrottle):
    """Limite le nombre de demandes par adresse IP (DEMANDES_THROTTLE_RATE)."""

    scope = "demandes"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


def _notifier(demande_id):
    close_old_connections()
    try:
        demande = Demande.objects.select_related("entreprise").get(pk=demande_id)
        notifier_nouvelle_demande(demande)
    except Exception:  # noqa: BLE001 — la demande est déjà enregistrée
        logger.exception("Erreur lors des notifications de la demande %s", demande_id)
    finally:
        close_old_connections()


def lancer_notifications(demande_id):
    if getattr(settings, "NOTIFICATIONS_ASYNC", True):
        threading.Thread(target=_notifier, args=(demande_id,), daemon=True).start()
    else:
        _notifier(demande_id)


@api_view(["POST"])
@throttle_classes([DemandesThrottle])
def creer_demande(request):
    serializer = DemandeCreateSerializer(
        data=request.data, context={"ip": DemandesThrottle().get_ident(request)}
    )
    serializer.is_valid(raise_exception=True)
    demande = serializer.save()
    transaction.on_commit(lambda: lancer_notifications(demande.pk))
    return Response(
        {"reference": demande.reference, "total_estime": demande.total_estime},
        status=status.HTTP_201_CREATED,
    )
