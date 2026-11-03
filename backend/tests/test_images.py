from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from catalog.models import Entreprise


@pytest.mark.django_db
def test_image_convertie_en_webp_et_reduite():
    buf = BytesIO()
    Image.new("RGB", (4000, 2000), "red").save(buf, "PNG")
    e = Entreprise(nom="Test", banniere=SimpleUploadedFile("Grosse Image.PNG", buf.getvalue()))
    e.save()
    assert e.banniere.name.endswith(".webp")
    with Image.open(e.banniere.path) as img:
        assert img.format == "WEBP" and max(img.size) == 1920
