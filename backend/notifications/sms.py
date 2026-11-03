"""Envoi de SMS via un fournisseur interchangeable.

Le fournisseur est choisi par la variable d'environnement SMS_PROVIDER :

- ``console`` (défaut) : n'envoie rien, écrit le SMS dans les logs. Pour le
  développement et en attendant l'ouverture d'un compte chez un fournisseur.
- ``twilio`` : API Twilio (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM
  ou SMS_SENDER_ID).
- ``techsoft`` : Techsoft SMS (Cameroun, app.techsoft-sms.com) — TECHSOFT_API_TOKEN
  et SMS_SENDER_ID (nom d'expéditeur enregistré chez Techsoft).
- ``http`` : agrégateur local générique. POST JSON
  ``{"to", "from", "message"}`` vers SMS_HTTP_URL avec l'en-tête
  ``Authorization: Bearer SMS_HTTP_TOKEN``. À adapter au format exact du
  fournisseur retenu (MTN/Orange/agrégateur) dans ``HttpProvider.send``.
"""

import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class SmsError(Exception):
    pass


def normaliser_numero(numero: str) -> str:
    """Renvoie le numéro au format international +237XXXXXXXXX."""
    brut = (numero or "").strip()
    chiffres = re.sub(r"\D", "", brut)
    if not chiffres:
        raise SmsError("Numéro vide.")
    if brut.startswith("+"):
        return "+" + chiffres
    if chiffres.startswith("00"):
        return "+" + chiffres[2:]
    indicatif = settings.SMS_DEFAULT_COUNTRY_CODE
    if chiffres.startswith(indicatif) and len(chiffres) > 9:
        return "+" + chiffres
    return f"+{indicatif}{chiffres}"


def numero_valide(numero: str) -> bool:
    try:
        n = normaliser_numero(numero)
    except SmsError:
        return False
    # Cameroun : 9 chiffres après +237 ; autres pays : 8 à 15 chiffres au total.
    if n.startswith("+237"):
        return len(n) == 13
    return 9 <= len(n) - 1 <= 15


class ConsoleProvider:
    def send(self, to, message):
        logger.info("[SMS console] → %s : %s", to, message)


class TwilioProvider:
    def send(self, to, message):
        sid, token = settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
        if not (sid and token):
            raise SmsError("Identifiants Twilio manquants.")
        reponse = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
            data={"To": to, "From": settings.TWILIO_FROM or settings.SMS_SENDER_ID, "Body": message},
            auth=(sid, token),
            timeout=15,
        )
        if reponse.status_code >= 300:
            raise SmsError(f"Twilio {reponse.status_code} : {reponse.text[:300]}")


class TechsoftProvider:
    """API HTTP de Techsoft SMS : POST JSON, numéro au format 237XXXXXXXXX."""

    def send(self, to, message):
        if not settings.TECHSOFT_API_TOKEN:
            raise SmsError("TECHSOFT_API_TOKEN n'est pas configuré.")
        try:
            reponse = requests.post(
                settings.TECHSOFT_API_URL,
                json={
                    "api_token": settings.TECHSOFT_API_TOKEN,
                    "recipient": to.lstrip("+"),
                    "sender_id": settings.SMS_SENDER_ID,
                    "type": "plain",
                    "message": message,
                },
                headers={"Accept": "application/json"},
                timeout=20,
            )
        except requests.RequestException as exc:
            raise SmsError(f"Techsoft injoignable : {exc}") from exc
        if reponse.status_code >= 300:
            raise SmsError(f"Techsoft {reponse.status_code} : {reponse.text[:300]}")
        # Certaines API répondent 200 avec une erreur dans le corps JSON.
        try:
            corps = reponse.json()
        except ValueError:
            return
        if isinstance(corps, dict) and str(corps.get("status", "")).lower() in ("error", "failed", "false"):
            raise SmsError(f"Techsoft a refusé le SMS : {corps.get('message') or corps}")


class HttpProvider:
    def send(self, to, message):
        if not settings.SMS_HTTP_URL:
            raise SmsError("SMS_HTTP_URL n'est pas configuré.")
        reponse = requests.post(
            settings.SMS_HTTP_URL,
            json={"to": to, "from": settings.SMS_SENDER_ID, "message": message},
            headers={"Authorization": f"Bearer {settings.SMS_HTTP_TOKEN}"},
            timeout=15,
        )
        if reponse.status_code >= 300:
            raise SmsError(f"Fournisseur SMS {reponse.status_code} : {reponse.text[:300]}")


PROVIDERS = {
    "console": ConsoleProvider,
    "techsoft": TechsoftProvider,
    "twilio": TwilioProvider,
    "http": HttpProvider,
}


def get_provider():
    try:
        return PROVIDERS[settings.SMS_PROVIDER]()
    except KeyError as exc:
        raise SmsError(f"Fournisseur SMS inconnu : {settings.SMS_PROVIDER}") from exc


def envoyer_sms(numero, message):
    get_provider().send(normaliser_numero(numero), message)
