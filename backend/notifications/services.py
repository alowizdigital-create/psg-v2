"""Notifications envoyées après chaque nouvelle demande client.

Trois destinataires :
1. le client (SMS de confirmation, + e-mail s'il a donné son adresse) ;
2. l'équipe de l'entreprise concernée (numéros/e-mails de l'entreprise et de
   ses gestionnaires) ;
3. les superadmins (et les contacts de supervision des réglages du site).

Chaque envoi est journalisé dans ``Notification`` : un échec n'empêche jamais
l'enregistrement de la demande et peut être relancé
(``manage.py retry_notifications``).
"""

import logging
from html import escape

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from catalog.models import SiteSettings

from .models import Notification
from .sms import SmsError, envoyer_sms, normaliser_numero

logger = logging.getLogger(__name__)

SMS_MAX = 459  # 3 segments GSM


def _separer(valeur):
    return [v.strip() for v in (valeur or "").replace(";", ",").split(",") if v.strip()]


def _cle_sms(numero):
    try:
        return normaliser_numero(numero)
    except SmsError:
        return numero


def _fcfa(montant):
    return f"{montant:,} FCFA".replace(",", " ") if montant else "sur devis"


def lien_admin(demande):
    base = settings.ADMIN_URL_FOR_LINKS
    return f"{base}/admin/demandes/demande/{demande.pk}/change/" if base else ""


def destinataires(demande):
    """Renvoie {"equipe": (sms, emails), "superadmin": (sms, emails)} sans doublons."""
    User = get_user_model()
    reglages = SiteSettings.charger()
    vus_sms, vus_mail = set(), set()

    def ajouter(liste_sms, liste_mail, sms=(), mails=()):
        for n in sms:
            cle = _cle_sms(n)
            if n and cle not in vus_sms:
                vus_sms.add(cle)
                liste_sms.append(n)
        for m in mails:
            cle = (m or "").lower()
            if m and cle not in vus_mail:
                vus_mail.add(cle)
                liste_mail.append(m)

    equipe_sms, equipe_mail = [], []
    entreprise = demande.entreprise
    if entreprise:
        ajouter(equipe_sms, equipe_mail, _separer(entreprise.telephone_equipe),
                _separer(entreprise.email_equipe))
        gestionnaires = User.objects.filter(
            is_active=True, is_superuser=False,
            profil__entreprises=entreprise, profil__recevoir_notifications=True,
        ).select_related("profil")
        for u in gestionnaires:
            ajouter(equipe_sms, equipe_mail, [u.profil.telephone], [u.email])

    admin_sms, admin_mail = [], []
    superadmins = User.objects.filter(
        is_active=True, is_superuser=True, profil__recevoir_notifications=True,
    ).select_related("profil")
    for u in superadmins:
        ajouter(admin_sms, admin_mail, [u.profil.telephone], [u.email])
    ajouter(admin_sms, admin_mail, _separer(reglages.supervision_telephones),
            _separer(reglages.supervision_emails))

    return {
        Notification.EQUIPE: (equipe_sms, equipe_mail),
        Notification.SUPERADMIN: (admin_sms, admin_mail),
    }


# --- Contenus -----------------------------------------------------------------

def sms_client(demande, reglages):
    try:
        texte = reglages.sms_confirmation_client.format(
            nom_site=reglages.nom, prenom=demande.prenom, nom=demande.nom,
            reference=demande.reference, offre=demande.offre_titre or "votre projet",
        )
    except (KeyError, IndexError, ValueError):
        texte = (f"{reglages.nom} : votre demande {demande.reference} est bien reçue. "
                 "Un membre de notre équipe vous appellera très bientôt.")
    return texte[:SMS_MAX]


def sms_equipe(demande):
    choix = ", ".join(c.libelle for c in demande.choix.all())
    texte = (f"Nouvelle demande {demande.reference} ({demande.entreprise or 'contact'}) : "
             f"{demande.offre_titre or 'demande de contact'}. Client : {demande.nom}, {demande.telephone}.")
    if choix:
        texte += f" Choix : {choix}."
    texte += " A rappeler rapidement."
    return texte[:SMS_MAX]


def email_equipe(demande):
    sujet = f"[{demande.reference}] Nouvelle demande — {demande.offre_titre or 'Contact'} — {demande.nom}"
    lignes = [
        f"Référence : {demande.reference}",
        f"Entreprise : {demande.entreprise or '—'}",
        f"Offre : {demande.offre_titre or 'Demande de contact'}",
        "",
        f"Client : {demande.nom}",
        f"Téléphone : {demande.telephone}",
        f"E-mail : {demande.email or '—'}",
        f"Date de l'événement : {demande.date_evenement:%d/%m/%Y}" if demande.date_evenement
        else "Date de l'événement : —",
        f"Lieu : {demande.lieu or '—'}",
        "",
        "Choix du client :",
        demande.resume_choix() or "(aucune option cochée)",
        "",
        f"Total estimé : {_fcfa(demande.total_estime)}",
        "",
        "Message :",
        demande.message or "—",
    ]
    if lien_admin(demande):
        lignes += ["", f"Voir dans l'admin : {lien_admin(demande)}"]
    texte = "\n".join(lignes)

    tel = escape(demande.telephone)
    wa = "".join(ch for ch in _cle_sms(demande.telephone) if ch.isdigit())
    choix_html = "".join(
        f"<tr><td style='padding:6px 10px;color:#6E5F60'>{escape(c.groupe)}</td>"
        f"<td style='padding:6px 10px'><b>{escape(c.libelle)}</b></td>"
        f"<td style='padding:6px 10px;text-align:right'>{escape(_fcfa(c.prix)) if c.prix else ''}</td></tr>"
        for c in demande.choix.all()
    ) or "<tr><td style='padding:6px 10px' colspan='3'>Aucune option cochée</td></tr>"
    html = f"""
<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1E1416">
  <div style="background:#6E1524;color:#fff;padding:18px 22px;border-radius:12px 12px 0 0">
    <div style="color:#F5B800;font-size:12px;letter-spacing:2px">NOUVELLE DEMANDE</div>
    <h2 style="margin:6px 0 0">{escape(demande.offre_titre or 'Demande de contact')}</h2>
    <div style="opacity:.85">{escape(demande.reference)} · {escape(str(demande.entreprise or ''))}</div>
  </div>
  <div style="border:1px solid #E8DCD6;border-top:0;padding:20px 22px;border-radius:0 0 12px 12px">
    <p style="margin:0 0 6px"><b>{escape(demande.nom)}</b></p>
    <p style="margin:0 0 6px">📞 <a href="tel:{tel}">{tel}</a> ·
       <a href="https://wa.me/{wa}">WhatsApp</a></p>
    <p style="margin:0 0 16px">✉️ {escape(demande.email or '—')}</p>
    <p style="margin:0 0 4px">📅 {demande.date_evenement.strftime('%d/%m/%Y') if demande.date_evenement else '—'}
       · 📍 {escape(demande.lieu or '—')}</p>
    <h3 style="margin:20px 0 8px">Choix du client</h3>
    <table style="width:100%;border-collapse:collapse;background:#F8F1EC;border-radius:8px">{choix_html}</table>
    <p style="font-size:18px;margin:16px 0"><b>Total estimé : {escape(_fcfa(demande.total_estime))}</b></p>
    <h3 style="margin:20px 0 8px">Message</h3>
    <p style="white-space:pre-line;margin:0">{escape(demande.message or '—')}</p>
    {f'<p style="margin-top:24px"><a href="{escape(lien_admin(demande))}" style="background:#F5B800;color:#1E1416;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:bold">Ouvrir dans l’admin</a></p>' if lien_admin(demande) else ''}
  </div>
</div>"""
    return sujet, texte, html


def email_client(demande, reglages):
    sujet = f"{reglages.nom} — votre demande {demande.reference} est bien reçue"
    texte = (
        f"Bonjour {demande.prenom},\n\n"
        f"Merci pour votre demande « {demande.offre_titre or 'contact'} » (référence {demande.reference}).\n"
        "Un membre de notre équipe vous appellera très bientôt pour en discuter.\n\n"
        f"Récapitulatif de vos choix :\n{demande.resume_choix() or '—'}\n\n"
        f"Total estimé : {_fcfa(demande.total_estime)} (indicatif, confirmé lors de l'appel).\n\n"
        f"À très vite,\nL'équipe {reglages.nom}"
    )
    return sujet, texte


# --- Envoi --------------------------------------------------------------------

def _envoyer(notification):
    notification.tentatives += 1
    try:
        if notification.canal == Notification.SMS:
            envoyer_sms(notification.destinataire, notification.contenu)
        else:
            html = getattr(notification, "_html", None)
            mail = EmailMultiAlternatives(
                notification.sujet, notification.contenu, settings.DEFAULT_FROM_EMAIL,
                [notification.destinataire],
            )
            if html:
                mail.attach_alternative(html, "text/html")
            mail.send(fail_silently=False)
    except Exception as exc:  # noqa: BLE001 — on journalise toute erreur d'envoi
        logger.warning("Échec d'envoi %s à %s : %s", notification.canal, notification.destinataire, exc)
        notification.statut = Notification.ECHEC
        notification.erreur = str(exc)[:2000]
    else:
        notification.statut = Notification.ENVOYE
        notification.erreur = ""
        notification.envoye_le = timezone.now()
    notification.save()
    return notification


def notifier_nouvelle_demande(demande):
    """Crée et envoie toutes les notifications d'une nouvelle demande."""
    reglages = SiteSettings.charger()
    a_envoyer = []

    def creer(canal, pour, destinataire, contenu, sujet="", html=None):
        n = Notification.objects.create(
            demande=demande, canal=canal, type_destinataire=pour,
            destinataire=destinataire, sujet=sujet, contenu=contenu,
        )
        n._html = html
        a_envoyer.append(n)

    creer(Notification.SMS, Notification.CLIENT, demande.telephone, sms_client(demande, reglages))
    if demande.email:
        sujet, texte = email_client(demande, reglages)
        creer(Notification.EMAIL, Notification.CLIENT, demande.email, texte, sujet)

    texte_sms = sms_equipe(demande)
    sujet, texte_mail, html = email_equipe(demande)
    for pour, (numeros, emails) in destinataires(demande).items():
        for numero in numeros:
            creer(Notification.SMS, pour, numero, texte_sms)
        for email in emails:
            creer(Notification.EMAIL, pour, email, texte_mail, sujet, html)

    for n in a_envoyer:
        _envoyer(n)
    return a_envoyer


def relancer(notification):
    """Renvoie une notification en échec (HTML reconstruit pour l'équipe)."""
    if notification.canal == Notification.EMAIL and notification.type_destinataire != Notification.CLIENT:
        notification._html = email_equipe(notification.demande)[2]
    return _envoyer(notification)
