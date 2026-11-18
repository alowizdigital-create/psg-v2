"""Ajoute les blocs animés à la page PS Digital d'un site déjà installé (une seule fois).

Sur une installation neuve, la base est vide à ce stade : rien n'est fait, et seed_contenu crée
directement la page avec ces blocs.
"""
from django.db import migrations


def creer(Section, Element, entreprise, data, ordre):
    data = dict(data)
    elements = data.pop("elements")
    section = Section.objects.create(page="entreprise", entreprise=entreprise, ordre=ordre, **data)
    for j, el in enumerate(elements):
        el = {k: v for k, v in el.items() if k != "image"}
        Element.objects.create(section=section, ordre=j, **el)
    return section


def ajouter(apps, schema_editor):
    from catalog.seed import contenu

    Entreprise = apps.get_model("catalog", "Entreprise")
    Section = apps.get_model("catalog", "Section")
    Element = apps.get_model("catalog", "ElementSection")
    e = Entreprise.objects.filter(slug="psdigital").first()
    if not e or Section.objects.filter(entreprise=e, type__in=["ouverture", "defilant", "survol"]).exists():
        return

    existantes = list(Section.objects.filter(entreprise=e).order_by("ordre", "id"))
    ordre = [creer(Section, Element, e, contenu.DIGITAL_OUVERTURE, 0)]
    defilant_place = False
    for s in existantes:
        # Les cartes détaillées d'origine (sans titre) deviennent la liste interactive.
        if s.type == "cartes" and not s.titre:
            s.type = "survol"
            s.sur_titre = contenu.DIGITAL_SURVOL["sur_titre"]
            s.titre = contenu.DIGITAL_SURVOL["titre"]
            s.save(update_fields=["type", "sur_titre", "titre"])
        ordre.append(s)
        if s.type == "tuiles" and not defilant_place:
            ordre.append(creer(Section, Element, e, contenu.DIGITAL_DEFILANT, 0))
            defilant_place = True
    if not defilant_place:
        ordre.append(creer(Section, Element, e, contenu.DIGITAL_DEFILANT, 0))
    for i, s in enumerate(ordre):
        Section.objects.filter(pk=s.pk).update(ordre=i)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0007_blocs_animes")]
    operations = [migrations.RunPython(ajouter, migrations.RunPython.noop)]
