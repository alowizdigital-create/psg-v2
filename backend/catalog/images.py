"""Optimisation automatique des images téléversées dans l'admin.

Chaque image est redimensionnée (côté le plus long limité) et convertie en
WebP, ce qui divise généralement le poids par 5 à 10 par rapport aux PNG/JPEG
d'origine — important pour les visiteurs sur connexion mobile.
"""

from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

WEBP_QUALITY = 82


def optimiser_image(field_file, max_side=1920):
    """Convertit en WebP le fichier d'un ImageField s'il vient d'être téléversé.

    Ne fait rien si le fichier est déjà enregistré (pas de re-compression à
    chaque sauvegarde) ou si c'est un SVG.
    """
    if not field_file or getattr(field_file, "_committed", True):
        return
    nom = Path(field_file.name)
    if nom.suffix.lower() == ".svg":
        return

    field_file.seek(0)
    with Image.open(field_file) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=WEBP_QUALITY, method=6)

    nouveau_nom = f"{nom.stem[:80]}.webp"
    field_file.save(nouveau_nom, ContentFile(buffer.getvalue()), save=False)


class ImagesOptimiseesMixin:
    """À combiner avec un modèle : liste les champs image à optimiser."""

    #: {"nom_du_champ": taille_max_en_pixels}
    IMAGES_A_OPTIMISER: dict[str, int] = {}

    def save(self, *args, **kwargs):
        for champ, taille in self.IMAGES_A_OPTIMISER.items():
            optimiser_image(getattr(self, champ), taille)
        super().save(*args, **kwargs)
