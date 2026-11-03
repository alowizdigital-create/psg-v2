from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Entreprise, GroupeOptions, HeroSlide, Offre, Option, Section, SiteSettings
from .serializers import (
    EntrepriseDetailSerializer,
    EntrepriseResumeSerializer,
    HeroSlideSerializer,
    OffreDetailSerializer,
    OffreResumeSerializer,
    SectionSerializer,
    SiteSettingsSerializer,
)

PAGES_PUBLIQUES = {Section.PAGE_ACCUEIL, Section.PAGE_A_PROPOS, Section.PAGE_CONTACT}


def offres_publiees():
    return (
        Offre.objects.filter(publiee=True, entreprise__active=True)
        .select_related("entreprise")
        .prefetch_related(
            Prefetch("groupes", queryset=GroupeOptions.objects.prefetch_related(
                Prefetch("options", queryset=Option.objects.all()))),
        )
    )


@api_view(["GET"])
def site(request):
    """Réglages, navigation et diaporama : tout ce qui est commun à chaque page."""
    return Response({
        "reglages": SiteSettingsSerializer(SiteSettings.charger()).data,
        "entreprises": EntrepriseResumeSerializer(Entreprise.objects.filter(active=True), many=True).data,
        "slides": HeroSlideSerializer(HeroSlide.objects.filter(visible=True), many=True).data,
    })


@api_view(["GET"])
def page(request, page):
    if page not in PAGES_PUBLIQUES:
        raise NotFound()
    sections = Section.objects.filter(page=page, visible=True).prefetch_related("elements")
    return Response({"page": page, "sections": SectionSerializer(sections, many=True).data})


@api_view(["GET"])
def entreprises(request):
    return Response(EntrepriseResumeSerializer(Entreprise.objects.filter(active=True), many=True).data)


@api_view(["GET"])
def entreprise_detail(request, slug):
    qs = Entreprise.objects.filter(active=True).prefetch_related(
        Prefetch("sections", queryset=Section.objects.prefetch_related("elements")),
        Prefetch("offres", queryset=offres_publiees()),
    )
    return Response(EntrepriseDetailSerializer(get_object_or_404(qs, slug=slug)).data)


@api_view(["GET"])
def offres(request):
    qs = offres_publiees()
    if slug := request.query_params.get("entreprise"):
        qs = qs.filter(entreprise__slug=slug)
    if request.query_params.get("mises_en_avant"):
        qs = qs.filter(mise_en_avant=True)
    return Response(OffreResumeSerializer(qs, many=True).data)


@api_view(["GET"])
def offre_detail(request, slug):
    qs = offres_publiees().prefetch_related("galerie")
    return Response(OffreDetailSerializer(get_object_or_404(qs, slug=slug)).data)
