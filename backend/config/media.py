"""Service des fichiers médias avec prise en charge des requêtes partielles (« Range »).

Indispensable pour les chansons : sans « Range », les navigateurs ne savent pas avancer ou reculer
dans un morceau. Les autres fichiers sont servis comme avant.
"""
import mimetypes
import os
import re

from django.conf import settings
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.utils._os import safe_join
from django.views.static import serve

PLAGE = re.compile(r"bytes=(\d*)-(\d*)$")


def media(request, path):
    try:
        chemin = safe_join(settings.MEDIA_ROOT, path)
    except Exception:
        raise Http404
    entete = request.headers.get("Range", "")
    if not entete or not os.path.isfile(chemin):
        return serve(request, path, document_root=settings.MEDIA_ROOT)

    taille = os.path.getsize(chemin)
    m = PLAGE.match(entete.strip())
    if not m or (not m.group(1) and not m.group(2)):
        return serve(request, path, document_root=settings.MEDIA_ROOT)
    if m.group(1):
        debut = int(m.group(1))
        fin = int(m.group(2)) if m.group(2) else taille - 1
    else:  # « bytes=-N » : les N derniers octets
        debut = max(taille - int(m.group(2)), 0)
        fin = taille - 1
    fin = min(fin, taille - 1)
    if debut > fin or debut >= taille:
        reponse = HttpResponse(status=416)
        reponse["Content-Range"] = f"bytes */{taille}"
        return reponse

    longueur = fin - debut + 1
    fichier = open(chemin, "rb")
    fichier.seek(debut)
    type_mime = mimetypes.guess_type(chemin)[0] or "application/octet-stream"
    reponse = StreamingHttpResponse(_morceau(fichier, longueur), status=206, content_type=type_mime)
    reponse["Content-Length"] = str(longueur)
    reponse["Content-Range"] = f"bytes {debut}-{fin}/{taille}"
    reponse["Accept-Ranges"] = "bytes"
    return reponse


def _morceau(fichier, longueur, bloc=64 * 1024):
    try:
        while longueur > 0:
            donnees = fichier.read(min(bloc, longueur))
            if not donnees:
                break
            longueur -= len(donnees)
            yield donnees
    finally:
        fichier.close()
