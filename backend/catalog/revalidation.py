"""Demande au site Next.js de rafraîchir ses pages après une modification dans l'admin."""

import logging
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _appeler():
    try:
        requests.post(
            f"{settings.FRONTEND_INTERNAL_URL}/revalidate",
            headers={"x-revalidate-secret": settings.FRONTEND_REVALIDATE_SECRET},
            timeout=5,
        )
    except requests.RequestException as exc:
        logger.info("Revalidation du site impossible (le cache expirera seul) : %s", exc)


def demander_revalidation():
    if settings.FRONTEND_REVALIDATE_SECRET:
        threading.Thread(target=_appeler, daemon=True).start()
