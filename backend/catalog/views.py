from urllib.parse import quote

from django.db.models import Prefetch
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Avis, Entreprise, GroupeOptions, HeroSlide, Offre, Option, Section, SiteSettings
from .serializers import (
    EntrepriseDetailSerializer,
    EntrepriseResumeSerializer,
    HeroSlideSerializer,
    OffreDetailSerializer,
    OffreResumeSerializer,
    SectionSerializer,
    SiteSettingsSerializer,
    resume_avis,
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


@api_view(["GET"])
def avis(request):
    """Avis publiés : ?accueil=1 pour ceux de la page d'accueil."""
    qs = Avis.objects.filter(publie=True).select_related("offre")
    if request.query_params.get("accueil"):
        qs = qs.filter(afficher_accueil=True)
    return Response(resume_avis(qs))


def avis_verifier(request, pk):
    """Redirige vers le WhatsApp du client, avec un message demandant de confirmer son avis.

    Le numéro n'apparaît jamais dans la page ni dans l'API : il n'est révélé que par cette
    redirection, et seulement si le client a donné son accord (case cochée dans l'admin).
    """
    if request.method != "GET":
        raise Http404()
    avis = get_object_or_404(Avis.objects.select_related("offre"), pk=pk, publie=True)
    if not avis.verifiable:
        raise Http404()
    prenom = avis.nom.split()[0]
    sujet = f" sur « {avis.offre.titre} »" if avis.offre_id else ""
    message = (
        f"Bonjour {prenom}, je viens de lire votre avis{sujet} sur le site de PS GROUP SARL. "
        "Pouvez-vous me confirmer que cet avis est bien de vous ? Merci !"
    )
    reponse = HttpResponseRedirect(f"https://wa.me/{avis.numero_whatsapp()}?text={quote(message)}")
    reponse["Cache-Control"] = "no-store"
    reponse["X-Robots-Tag"] = "noindex, nofollow"
    reponse["Referrer-Policy"] = "no-referrer"
    return reponse
