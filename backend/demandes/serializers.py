from django.db import transaction
from rest_framework import serializers

from catalog.models import Entreprise, GroupeOptions, Offre, Option
from notifications.sms import numero_valide

from .models import Demande, DemandeChoix


class DemandeCreateSerializer(serializers.Serializer):
    """Demande envoyée depuis le site public.

    Les prix et libellés ne sont jamais pris dans la requête : ils sont relus
    en base à partir des identifiants d'options, puis copiés dans la demande.
    """

    offre = serializers.SlugField(required=False, allow_blank=True)
    entreprise = serializers.SlugField(required=False, allow_blank=True)
    nom = serializers.CharField(max_length=120, trim_whitespace=True)
    telephone = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=False, allow_blank=True)
    date_evenement = serializers.DateField(required=False, allow_null=True)
    lieu = serializers.CharField(max_length=160, required=False, allow_blank=True)
    message = serializers.CharField(max_length=3000, required=False, allow_blank=True)
    choix = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False,
                                  max_length=100, default=list)
    # Champ piège invisible pour les robots : doit rester vide.
    site_web = serializers.CharField(required=False, allow_blank=True)

    def validate_nom(self, valeur):
        if len(valeur.strip()) < 2:
            raise serializers.ValidationError("Indiquez votre nom.")
        return valeur.strip()

    def validate_telephone(self, valeur):
        if not numero_valide(valeur):
            raise serializers.ValidationError("Numéro de téléphone invalide (ex. 6 53 83 43 02).")
        return valeur.strip()

    def validate_site_web(self, valeur):
        if valeur:
            raise serializers.ValidationError("Requête refusée.")
        return valeur

    def validate(self, data):
        offre = None
        entreprise = None
        if data.get("offre"):
            offre = (Offre.objects.filter(slug=data["offre"], publiee=True, entreprise__active=True)
                     .select_related("entreprise").first())
            if not offre:
                raise serializers.ValidationError({"offre": "Cette offre n'est plus disponible."})
            entreprise = offre.entreprise
        elif data.get("entreprise"):
            entreprise = Entreprise.objects.filter(slug=data["entreprise"], active=True).first()

        ids = list(dict.fromkeys(data.get("choix") or []))
        options = []
        if ids:
            if not offre:
                raise serializers.ValidationError({"choix": "Des options ont été envoyées sans offre."})
            par_id = {
                o.id: o for o in Option.objects.filter(
                    id__in=ids, groupe__offre=offre, disponible=True,
                ).select_related("groupe")
            }
            if len(par_id) != len(ids):
                raise serializers.ValidationError(
                    {"choix": "Certaines options ne sont plus disponibles. Rechargez la page."})
            options = [par_id[i] for i in ids]

        if offre:
            erreurs = {}
            for groupe in offre.groupes.prefetch_related("options"):
                if not any(o.disponible for o in groupe.options.all()):
                    continue
                n = sum(1 for o in options if o.groupe_id == groupe.id)
                if groupe.obligatoire and n == 0:
                    erreurs[str(groupe.id)] = f"Choisissez une option pour « {groupe.libelle} »."
                if groupe.type == GroupeOptions.UNIQUE and n > 1:
                    erreurs[str(groupe.id)] = f"Un seul choix possible pour « {groupe.libelle} »."
            if erreurs:
                raise serializers.ValidationError({"groupes": erreurs})

        data["_offre"], data["_entreprise"], data["_options"] = offre, entreprise, options
        return data

    @staticmethod
    def calculer_total(offre, options):
        montants = [offre.prix_a_partir_de] if offre else []
        montants += [o.prix for o in options]
        montants = [m for m in montants if m]
        return sum(montants) if montants else None

    @transaction.atomic
    def create(self, data):
        offre, entreprise, options = data["_offre"], data["_entreprise"], data["_options"]
        options.sort(key=lambda o: (o.groupe.ordre, o.groupe.id, o.ordre, o.id))
        demande = Demande.objects.create(
            offre=offre,
            entreprise=entreprise,
            offre_titre=offre.titre if offre else "",
            nom=data["nom"],
            telephone=data["telephone"],
            email=data.get("email", ""),
            date_evenement=data.get("date_evenement"),
            lieu=data.get("lieu", ""),
            message=data.get("message", ""),
            total_estime=self.calculer_total(offre, options),
            ip=self.context.get("ip"),
        )
        DemandeChoix.objects.bulk_create([
            DemandeChoix(demande=demande, option=o, groupe=o.groupe.libelle, libelle=o.libelle,
                         prix=o.prix, ordre=i)
            for i, o in enumerate(options)
        ])
        return demande
