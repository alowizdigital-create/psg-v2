"""Contenu repris du premier site (psg) pour initialiser la base.

Tout ce contenu reste ensuite modifiable dans l'admin. Les fautes de frappe
du premier site ont été corrigées au passage. Les offres du catalogue et leurs
prix sont des EXEMPLES à adapter par l'équipe.
"""

REGLAGES = {
    "nom": "PS GROUP SARL",
    "slogan": "L'innovation au service de vos ambitions",
    "devise_pied": "La vision du futur.",
    "adresse": "Petit Marché ODZA, Face école Léo, Yaoundé",
    "telephones": "653 834 302, 655 934 760",
    "email": "infos.pointsolutionsgroup@gmail.com",
    "whatsapp": "237655334760",
    # Liens des réseaux du groupe : à compléter dans l'admin (le premier site
    # pointait vers les pages d'accueil génériques de Facebook, Instagram…).
    "facebook": "",
    "instagram": "",
    "tiktok": "",
    "youtube": "",
}

SLIDES = ["slides/slide-1.webp", "slides/slide-2.webp", "slides/slide-3.webp", "slides/slide-4.webp"]


def S(type, sur_titre="", titre="", texte="", elements=(), **extra):
    return {"type": type, "sur_titre": sur_titre, "titre": titre, "texte": texte,
            "elements": list(elements), **extra}


def E(titre="", sous_titre="", texte="", icone="", image="", lien="", en_avant=False):
    return {"titre": titre, "sous_titre": sous_titre, "texte": texte, "icone": icone,
            "image": image, "lien": lien, "en_avant": en_avant}


PAGES = {
    "accueil": [
        S("chiffres", elements=[
            E("6", "Entreprises réunies"),
            E("1.3K+", "Abonnés qui nous suivent"),
            E("100%", "Créations sur mesure"),
            E("1", "Groupe, une seule ambition"),
        ]),
        S("cartes", "Qui sommes-nous ?", "Un groupe | Plusieurs expertises | Une seule équipe",
          "PS GROUP SARL rassemble des spécialistes formés par secteur pour accompagner vos projets "
          "du concept à la réalisation, avec exigence et créativité.",
          elements=[
              E("Expertise sectorielle", texte="Chaque entreprise du groupe est portée par des spécialistes "
                "formés à son secteur, pour un résultat professionnel à chaque étape.", icone="award"),
              E("Vision commune", texte="Toutes nos branches partagent la même ambition : rendre vos "
                "projets et vos événements uniques, avec innovation.", icone="target"),
              E("Accompagnement global", texte="De l'étude du projet à la production audiovisuelle, "
                "jusqu'à la diffusion média : un seul interlocuteur pour couvrir l'ensemble de vos besoins.",
                icone="handshake"),
          ]),
        S("entreprises", "Nos entreprises", "Les 6 branches de PS GROUP SARL",
          "Cliquez sur une entreprise pour découvrir son activité en détail.", fond_alterne=True),
        S("offres", "Catalogue", "Composez votre prestation sur mesure",
          "Choisissez une offre, cochez les options qui vous intéressent et envoyez votre demande : "
          "un membre de notre équipe vous rappelle.",
          bouton_label="Voir tout le catalogue", bouton_lien="/catalogue"),
        S("cta", titre="Un projet en tête ? Parlons-en.",
          texte="Notre équipe est prête à donner vie à vos ambitions, quel que soit le domaine.",
          bouton_label="Nous contacter", bouton_lien="/contact"),
    ],
    "a-propos": [
        S("entete", "À propos", "Qui sommes-nous ?",
          "PS GROUP SARL est bien plus qu'une simple agence événementielle et marketing. Spécialisée dans "
          "l'organisation d'événements de mariage et d'entreprise, notre équipe basée à Yaoundé opère "
          "dans tout le Cameroun."),
        S("personnes", "Notre équipe", "Les visages derrière PS GROUP SARL",
          "Faites connaissance avec quelques-uns des membres qui rendent tout cela possible.",
          colonnes=4, elements=[
              E("Leader Washi", "CEO, PS GROUP SARL", image="equipes/leader.webp", en_avant=True),
              E("Iness Nono", "Project Coordinator", image="equipes/iness.webp"),
              E("Ted E. Mbang", "Manager IT & Team Leadership", image="equipes/ted.webp"),
              E("Serge Sodong Sodong", "Photography Service Manager", image="equipes/serge.webp"),
              E("Fabrice Ondoa", "Video Editor", image="equipes/fabrice.webp"),
          ]),
        S("texte", "Notre approche", "Une approche sur-mesure, du concept à la réalisation",
          "Que ce soit pour un lancement de produit, une inauguration, une soirée de gala ou une "
          "conférence, nous analysons attentivement vos besoins pour concevoir un événement innovant, "
          "créatif et en parfaite adéquation avec votre identité.\n\n"
          "En plus de notre expertise interne, nous agissons également en tant que passerelle vers une "
          "multitude de prestataires de qualité, vous offrant ainsi un accès à des idées originales et des "
          "services haut de gamme. Faites confiance à notre savoir-faire pour communiquer votre message "
          "avec impact, remodeler votre image de marque et éblouir vos invités à chaque occasion.",
          titre_encadre="En bref", elements=[
              E("Basé à Yaoundé, opérant dans tout le Cameroun", icone="map-pin"),
              E("Fondée le 1er août 2022", icone="calendar"),
              E("SARL enregistrée officiellement depuis 2023", icone="building-2"),
              E("Plusieurs entreprises : PS Studio Créative, PS Digital, PSG ZIK, AFRIJEUNE TV…",
                icone="layers"),
          ]),
        S("chiffres", elements=[
            E("75", "Projets réalisés"), E("50", "Clients accompagnés"), E("20", "Partenariats"),
        ]),
        S("texte", "Notre histoire", "Une aventure lancée en 2022",
          "Fondée le 1er août 2022 par la vision d'un jeune Camerounais désireux d'apporter une nouvelle "
          "perspective à l'événementiel à travers le design, la photographie et le digital, avec des "
          "projets tels que PS Studio Créative, PS Digital, PSG ZIK, AFRIJEUNE TV et bien d'autres, "
          "touchant toutes les populations du pays. PS GROUP SARL représente l'aboutissement de nombreuses "
          "années de travail, combinant des compétences techniques qualifiées et une expertise "
          "professionnelle. Depuis 2023, PS GROUP SARL est officiellement enregistrée en tant que société "
          "à responsabilité limitée (SARL).", fond_alterne=True),
        S("cartes", "Comment nous travaillons", "Une approche collaborative et personnalisée",
          "Nous croyons en une approche collaborative et personnalisée pour chaque projet, mettant "
          "l'accent sur la transparence, l'innovation et la qualité.", colonnes=2, fond_alterne=True,
          elements=[
              E("Approche holistique et collaborative", icone="workflow", texte=(
                  "Nous adoptons une approche intégrée pour chaque projet, en commençant par une "
                  "compréhension approfondie de vos besoins, objectifs et public cible. Cette analyse guide "
                  "notre conception stratégique, où nous utilisons les dernières tendances pour créer une "
                  "stratégie personnalisée. Nous favorisons une collaboration active tout au long du "
                  "processus, avec une communication ouverte et régulière.")),
              E("Cycle complet de réussite", icone="circle-check", texte=(
                  "Nous débutons chaque projet par une compréhension approfondie de vos besoins, puis "
                  "mettons en œuvre la stratégie conçue avec minutie, garantissant une qualité "
                  "exceptionnelle à chaque étape. Nous restons flexibles et réceptifs aux retours pour "
                  "assurer une amélioration continue. Une fois le projet terminé, nous célébrons sa réussite "
                  "avec vous et restons disponibles pour tout support supplémentaire.")),
          ]),
        S("cta", titre="Envie d'en savoir plus sur nos entreprises ?",
          texte="Découvrez chacune des branches de PS GROUP SARL en détail.",
          bouton_label="Voir nos entreprises", bouton_lien="/#entreprises"),
    ],
    "contact": [
        S("entete", "Contact", "Parlons de votre projet",
          "Une question, un projet, une envie de collaboration ? Notre équipe vous répond rapidement."),
    ],
}


ENTREPRISES = [
    {
        "slug": "pscreative",
        "nom": "PS Studio Créative",
        "sur_titre": "Nos entreprises — PS Studio Créative",
        "accroche": "Découvrez notre studio créatif.",
        "resume": "Captation, montage et réalisation de contenus audiovisuels professionnels.",
        "icone": "clapperboard",
        "banniere": "pscreative/creative.webp",
        "cta_titre": "Un projet audiovisuel en tête ?",
        "cta_texte": "Parlons de votre projet et donnons-lui vie ensemble.",
        "sections": [
            S("galerie", "Portfolio", "Nos réalisations",
              "Un aperçu de nos shootings photo réalisés pour nos clients.", fond_alterne=True, colonnes=4,
              elements=[
                  E("Shooting beauté", image="pscreative/shooting1.webp"),
                  E("Shooting anniversaire", image="pscreative/shooting2.webp"),
                  E("Shooting anniversaire", image="pscreative/shootinghbhomme.webp"),
                  E("Shooting enfant", image="pscreative/shootingenfant.webp"),
                  E("Shooting mariage", image="pscreative/shootingmariage.webp"),
                  E("Shooting grossesse", image="pscreative/shootingrossesse.webp"),
                  E("Préparatifs de mariage", image="pscreative/shootongmariage2.webp"),
                  E("Shooting homme", image="pscreative/shootinhomm.webp"),
              ]),
            S("cartes", "Services de photographie & audiovisuel", "Des images qui marquent",
              "Notre studio créatif offre une gamme complète de services de photographie et d'audiovisuel "
              "pour capturer vos moments spéciaux avec éclat. Que ce soit pour des portraits, des événements "
              "ou des projets commerciaux, notre équipe expérimentée garantit des résultats exceptionnels.",
              elements=[
                  E("Shooting photo pro", icone="camera", texte=(
                      "Nos séances de shooting photo professionnelles sont conçues pour capturer vos moments "
                      "les plus précieux avec une qualité exceptionnelle, pour des portraits, événements "
                      "spéciaux ou projets commerciaux.")),
                  E("Couverture de mariages", icone="wine", texte=(
                      "De la cérémonie à la réception, nous documentons chaque instant de bonheur, d'émotion "
                      "et d'amour, avec une approche discrète et artistique pour des souvenirs intemporels.")),
                  E("Réalisation de spots vidéo", icone="megaphone", texte=(
                      "Des spots publicitaires percutants pour promouvoir votre entreprise, produit ou "
                      "service, de la conception du scénario à la post-production.")),
                  E("Clip vidéo", icone="music", texte=(
                      "Des clips vidéo uniques et engageants pour les artistes musicaux, influenceurs ou "
                      "entreprises, qui captivent l'audience et renforcent la présence en ligne.")),
                  E("Films & court métrage", icone="film", texte=(
                      "Du concept à la réalisation, nous créons des films et courts métrages qui racontent "
                      "des histoires fascinantes et inspirantes, pour le divertissement ou la promotion.")),
                  E("Formation aux métiers audiovisuels", icone="graduation-cap", texte=(
                      "Des formations spécialisées et pratiques, dispensées par des professionnels "
                      "expérimentés, pour maîtriser la production vidéo, le montage et la prise de vue.")),
              ]),
        ],
    },
    {
        "slug": "psdigital",
        "nom": "PS Digital",
        "sur_titre": "Nos entreprises — PS Digital",
        "accroche": "Explorez nos services de marketing digital.",
        "resume": "Réseaux sociaux, développement web, infographie & print, hébergement et modélisation 2D/3D.",
        "icone": "hash",
        "banniere": "pscreative/psdigit.webp",
        "cta_titre": "Prêt à développer votre présence digitale ?",
        "cta_texte": "Parlons de votre stratégie de communication.",
        "sections": [
            S("tuiles", "Services de marketing digital", "Développer votre visibilité en ligne",
              "Une gamme complète de services de marketing digital pour aider votre entreprise à prospérer "
              "dans le monde numérique d'aujourd'hui : de la gestion des médias sociaux à la création de "
              "campagnes publicitaires percutantes.", colonnes=4, elements=[
                  E("Création et gestion des pages réseaux sociaux", icone="users"),
                  E("Validation et monétisation de comptes", icone="badge-check"),
                  E("Sponsoring & boost", icone="megaphone"),
                  E("Développement web", icone="code"),
                  E("Infographie & print", icone="chart-column"),
                  E("Hébergement web", icone="server"),
                  E("Filtres Snapchat", icone="ghost"),
                  E("Modélisation 2D & 3D", icone="box"),
              ]),
            S("cartes", elements=[
                E("Création et gestion des pages réseaux sociaux", texte=(
                    "Nous créons et gérons des pages professionnelles sur les réseaux sociaux pour renforcer "
                    "votre présence en ligne. De la conception de contenu à l'interaction avec les abonnés, "
                    "nous veillons à ce que vos plateformes sociales reflètent votre marque et atteignent "
                    "votre public cible.")),
                E("Validation et monétisation de comptes", texte=(
                    "Nous vous aidons à obtenir la validation des comptes sur les plateformes sociales pour "
                    "renforcer votre crédibilité et votre visibilité en ligne. Grâce à nos stratégies "
                    "éprouvées, nous maximisons vos chances d'obtenir la reconnaissance officielle de votre "
                    "marque ou de votre profil.")),
                E("Sponsoring & boost", texte=(
                    "Boostez la visibilité de vos publications et atteignez un public plus large grâce à nos "
                    "services de sponsoring et de boost. Nous optimisons vos campagnes publicitaires pour "
                    "maximiser votre retour sur investissement et vous aider à atteindre vos objectifs "
                    "marketing.")),
                E("Développement web", texte=(
                    "Faites passer votre présence en ligne au niveau supérieur avec notre service de "
                    "développement web sur mesure. Notre équipe de développeurs expérimentés crée des sites "
                    "web dynamiques, réactifs et conviviaux, adaptés à vos besoins spécifiques et conçus pour "
                    "maximiser l'engagement et la conversion de vos visiteurs.")),
                E("Infographie & print", texte=(
                    "De la création d'infographies percutantes à la conception de supports d'impression de "
                    "qualité, nous vous proposons des services d'infographie et d'impression pour renforcer "
                    "votre communication visuelle. Nos graphistes talentueux transforment vos idées en "
                    "designs accrocheurs qui captivent votre public.")),
                E("Hébergement web", texte=(
                    "Assurez-vous que votre site web fonctionne de manière optimale avec nos services "
                    "d'hébergement web fiables et performants. Nous proposons des solutions d'hébergement "
                    "sécurisées et évolutives pour garantir la disponibilité et la rapidité de votre site, "
                    "offrant ainsi une expérience utilisateur optimale à vos visiteurs.")),
                E("Filtres Snapchat", texte=(
                    "Engagez votre public sur Snapchat avec des filtres personnalisés qui reflètent votre "
                    "marque ou votre événement. Nous concevons des filtres Snapchat uniques et créatifs pour "
                    "vous aider à interagir avec votre audience et à renforcer votre présence sur cette "
                    "plateforme populaire.")),
                E("Modélisation 2D & 3D", texte=(
                    "Explorez de nouvelles dimensions avec notre service de modélisation 2D & 3D. Que ce soit "
                    "pour des illustrations, des animations ou des projets de design, notre équipe de "
                    "modélisation crée des visuels époustouflants qui donnent vie à vos idées et captivent "
                    "votre public.")),
            ]),
        ],
    },
    {
        "slug": "formation",
        "nom": "Formation — Class of Week",
        "sur_titre": "Nos entreprises — Formation",
        "accroche": "Apprenez les métiers de la création avec nos experts.",
        "resume": "Des formations animées par des spécialistes, par secteur d'activité.",
        "icone": "graduation-cap",
        "banniere": "pscreative/creative.webp",
        "cta_titre": "Envie de rejoindre une prochaine session ?",
        "cta_texte": "Contactez-nous pour connaître le programme et les prochaines dates.",
        "sections": [
            S("cartes", "Notre expertise", "Se former aux métiers du groupe PS GROUP SARL",
              "Class of Week propose des formations spécialisées, dispensées par des professionnels "
              "expérimentés de chaque entreprise du groupe, pour vous fournir les connaissances et "
              "compétences nécessaires pour réussir dans l'industrie.", elements=[
                  E("Audiovisuel", icone="clapperboard", image="pscreative/creative.webp", texte=(
                      "Production, prise de vue, montage & post-production, avec les experts de PS Studio "
                      "Créative.")),
                  E("Digital & réseaux sociaux", icone="hash", image="pscreative/psdigit.webp", texte=(
                      "Gestion de pages, marketing digital et création de contenu, avec l'équipe PS "
                      "Digital.")),
                  E("Musique & production", icone="music", image="pscreative/micro.webp", texte=(
                      "Enregistrement, mastering et accompagnement d'artistes, avec les équipes de PSG ZIK.")),
                  E("Média & présentation TV", icone="tv", image="pscreative/afritiv.webp", texte=(
                      "Communication télévisée, reportage et présentation, avec l'équipe d'AFRIJEUNE TV.")),
                  E("Événementiel", icone="wine", image="evenementiel/reception.svg", texte=(
                      "Organisation, logistique et animation d'événements, du concept à la réalisation.")),
                  E("Infographie & création visuelle", icone="palette", image="pscreative/creative.webp",
                    texte="Identité visuelle, logos et supports graphiques, avec les créatifs du groupe."),
              ]),
            S("personnes", "Nos lauréats", "Ils ont suivi une formation Class of Week",
              "Rejoignez les prochaines promotions et développez vos compétences avec nos experts.",
              fond_alterne=True, colonnes=4, elements=[
                  E("Promotion Audiovisuel", "Session 2025", image="formation/illustration-1.webp"),
                  E("Promotion Digital", "Session 2025", image="formation/illustration-2.webp"),
                  E("Promotion Événementiel", "Session 2025", image="formation/laureat1.webp"),
                  E("Promotion Événementiel", "Session 2025", image="formation/laureat2.webp"),
              ]),
        ],
    },
    {
        "slug": "pszik",
        "nom": "PSG ZIK",
        "sur_titre": "Nos entreprises — PSG ZIK",
        "accroche": "Découvrez nos services dédiés à l'industrie musicale.",
        "resume": "Production et management d'artistes, enregistrement, mastering et distribution musicale.",
        "icone": "music",
        "banniere": "pscreative/micro.webp",
        "cta_titre": "Un projet musical à concrétiser ?",
        "cta_texte": "Parlons de votre carrière ou de votre production musicale.",
        "sections": [
            S("personnes", "Inspiration", "Icônes de la musique camerounaise",
              "Des artistes qui ont marqué et font rayonner la musique camerounaise, toutes générations et "
              "tous genres confondus — une richesse qui inspire notre travail chez PSG ZIK.",
              fond_alterne=True, colonnes=4, elements=[
                  E("Manu Dibango", "Jazz & afrobeat — « Soul Makossa »", image="pssik/manudibango.webp"),
                  E("Lady Ponce", "Bikutsi & musique urbaine", image="pssik/ladyponce.webp"),
                  E("Mani Bella", "Afrobeat & musique urbaine", image="pssik/manibella.webp"),
                  E("Tenor", "Afrobeat & nouvelle scène", image="pssik/tenor.webp"),
              ]),
            S("cartes", "Service d'accompagnement musical", "Au service des artistes et de la musique",
              "De la production à la distribution, nous offrons un accompagnement personnalisé pour aider "
              "les artistes et les professionnels de l'industrie musicale à réussir dans le monde de la "
              "musique.", elements=[
                  E("Production et management d'artistes", icone="star", texte=(
                      "Nous offrons une gestion complète des artistes, de la recherche de talents à leur "
                      "développement et leur représentation. Avec notre expertise dans l'industrie musicale, "
                      "nous aidons les artistes à atteindre leur plein potentiel et à réussir dans une "
                      "industrie compétitive.")),
                  E("Communication musicale", icone="megaphone", texte=(
                      "Nous proposons des services de communication musicale pour promouvoir les artistes et "
                      "leurs projets. De la création de stratégies de communication à la gestion des relations "
                      "publiques, nous aidons les artistes à accroître leur visibilité et leur notoriété dans "
                      "l'industrie.")),
                  E("Enregistrement & mastering", icone="mic", texte=(
                      "Nous offrons des services d'enregistrement et de mastering de haute qualité pour "
                      "garantir que les projets musicaux atteignent leur plein potentiel sonore. Avec notre "
                      "équipement de pointe et notre expertise technique, nous assurons des résultats "
                      "professionnels à chaque étape du processus.")),
                  E("Distribution musicale", icone="satellite-dish", texte=(
                      "Nous proposons des services de distribution musicale pour aider les artistes à partager "
                      "leur musique avec un public mondial. Grâce à nos partenariats avec les principales "
                      "plateformes de streaming et de téléchargement, nous aidons les artistes à toucher un "
                      "large auditoire et à maximiser leur potentiel de revenus.")),
                  E("Facilitation", icone="handshake", texte=(
                      "Nous facilitons toutes les étapes du processus créatif et de production musicale. De la "
                      "planification des sessions d'enregistrement à la coordination des collaborations "
                      "artistiques, nous offrons un soutien complet pour que les projets musicaux se "
                      "concrétisent avec succès.")),
              ]),
        ],
    },
    {
        "slug": "concours",
        "nom": "Concours Miss Afrijeune",
        "sur_titre": "Nos entreprises — Concours",
        "accroche": "Une plateforme au service de la jeunesse africaine.",
        "resume": "Miss Afrijeune : une plateforme de valorisation de la jeunesse africaine sur 8 semaines.",
        "icone": "crown",
        "banniere": "pscreative/misstiv.webp",
        "cta_titre": "Envie de participer à la prochaine édition ?",
        "cta_texte": "Contactez-nous pour connaître les modalités d'inscription.",
        "sections": [
            S("personnes", "Miss Afrijeune", "Découvrez la cour",
              "La reine et sa cour, ambassadrices de la jeunesse africaine pour cette édition.", colonnes=4,
              elements=[
                  E("Miss Afrijeune+", image="pscreative/afri1.webp"),
                  E("Première Dauphine", image="pscreative/afri2.webp"),
                  E("Deuxième Dauphine", image="pscreative/afri3.webp"),
                  E("Miss Extrême", image="pscreative/afri4.webp"),
              ]),
            S("cartes", "Actualités", "Suivez le concours Miss Afrijeune", fond_alterne=True, colonnes=4,
              elements=[
                  E("Miss Afrijeune, bien plus qu'un concours de beauté", "Présentation", icone="crown",
                    image="pscreative/missafri.webp", texte=(
                        "Une plateforme sur 8 semaines dédiée à la valorisation des médias et de la jeunesse "
                        "africaine.")),
                  E("Comment participer à la prochaine édition", "Inscriptions", icone="square-pen",
                    image="pscreative/misstiv.webp", texte=(
                        "Éligibilité, inscription et audition : toutes les étapes pour rejoindre l'aventure.")),
                  E("Les lots qui attendent les lauréates", "Récompenses", icone="gift",
                    image="pscreative/lady.webp", texte=(
                        "Contrat de sponsoring, séjour en hôtel et cadeaux de luxe pour cette édition.")),
                  E("Une ambassadrice de la jeunesse africaine", "Le mandat", icone="crown",
                    image="pscreative/mani.webp", texte=(
                        "Découvrez le rôle et les engagements de Miss Afrijeune tout au long de son mandat.")),
              ]),
            S("liens", elements=[
                E("Suivez AFRIJEUNE TV sur Facebook", icone="", lien="https://web.facebook.com/Afrijeunetv"),
            ], fond_alterne=True),
            S("cartes", "C'est quoi Miss Afrijeune ?", "Bien plus qu'un concours de beauté",
              "Miss Afrijeune est une plateforme qui s'étend sur huit (8) semaines, chaque semaine étant "
              "dédiée à une activité spécifique. Ses objectifs incluent la valorisation des médias, la lutte "
              "contre la sous-information, la promotion de l'information de qualité et l'égalité médiatique. "
              "En mettant en lumière les talents et les réalisations des jeunes femmes, Miss Afrijeune "
              "inspire les générations futures et contribue à façonner un avenir prometteur pour le "
              "continent africain.", elements=[
                  E("Éligibilité", icone="list-checks", texte=(
                      "Jeunes femmes de tous les pays d'Afrique, sous réserve de répondre aux critères établis "
                      "(âge, nationalité, taille, éducation, etc.).")),
                  E("Inscription", icone="square-pen", texte=(
                      "En ligne ou directement à l'agence, avec vos informations personnelles et un portfolio "
                      "(photos, vidéos, réalisations, engagements sociaux).")),
                  E("Audition", icone="video", texte=(
                      "En présentiel ou en ligne pour les candidates hors de la ville, sur rendez-vous avec "
                      "notre équipe.")),
              ]),
            S("cartes", "Lots à gagner", "De belles récompenses à la clé", fond_alterne=True, elements=[
                E("Contrat de sponsoring", icone="file-signature", texte=(
                    "Un contrat exclusif avec PS GROUP SARL, offrant des opportunités de promotion d'image et "
                    "de sponsoring.")),
                E("Séjour en hôtel", icone="hotel", texte=(
                    "La deuxième dauphine bénéficie d'un séjour de deux jours et deux nuits, tous frais pris en "
                    "charge.")),
                E("Cadeaux de luxe", icone="gift", texte=(
                    "Un smartphone haut de gamme et une somme d'argent pour la gagnante, ainsi qu'un "
                    "accompagnement personnalisé dans ses projets.")),
            ]),
            S("texte", "Le mandat", "Une ambassadrice de la jeunesse africaine",
              "La gagnante est couronnée lors de la grande finale par un jury évaluant charisme, éloquence, "
              "beauté et engagement envers des causes sociales. Elle devient ambassadrice de la jeunesse "
              "africaine et porte-parole des initiatives Miss Afrijeune, avec un programme d'activités : "
              "événements caritatifs, conférences, séances de sensibilisation et plus encore."),
        ],
    },
    {
        "slug": "afrijeune-plus",
        "nom": "AFRIJEUNE TV",
        "sur_titre": "Nos entreprises — Média",
        "accroche": "Notre chaîne, dédiée à la jeunesse africaine.",
        "resume": "Notre chaîne de streaming en ligne dédiée à la jeunesse et à ses contenus.",
        "icone": "satellite-dish",
        "banniere": "pscreative/afritiv.webp",
        "cta_titre": "Envie de collaborer avec AFRIJEUNE TV ?",
        "cta_texte": "Contactez-nous pour en savoir plus sur notre chaîne média.",
        "sections": [
            S("texte", "Service de diffusion télévisée", "Une programmation pensée pour la jeunesse africaine",
              "AFRIJEUNE TV propose une programmation variée axée sur les intérêts et les préoccupations de "
              "la jeunesse africaine. De l'actualité aux divertissements, nous offrons une plateforme "
              "dynamique pour mettre en lumière les talents et les histoires de la jeunesse africaine."),
            S("liens", elements=[
                E("AFRIJEUNE TV sur Facebook", lien="https://web.facebook.com/Afrijeunetv?locale=fr_FR"),
                E("Dernières émissions sur YouTube", lien="https://www.youtube.com/@afrijeunetv"),
            ]),
            S("lignes", elements=[
                E("Communication télévisée", image="pscreative/televise.webp", texte=(
                    "Nous offrons des services de communication télévisée pour aider les entreprises, les "
                    "organisations et les individus à transmettre leurs messages à un large public à travers "
                    "nos plateformes de diffusion. De la production de contenu à la diffusion, nous assurons "
                    "une visibilité maximale pour vos initiatives.")),
                E("Publicités", image="pscreative/pub.webp", texte=(
                    "Nous proposons des services de publicité pour promouvoir les produits et les services "
                    "auprès de notre audience jeune et dynamique. Que ce soit pour une publicité télévisée "
                    "traditionnelle ou des partenariats de contenu, nous offrons des solutions de marketing "
                    "efficaces pour atteindre votre public cible.")),
                E("Reportages", image="pscreative/reportage.webp", texte=(
                    "Notre équipe de journalistes propose des reportages complets sur les événements et les "
                    "problématiques qui touchent la jeunesse africaine. Des sujets d'actualité aux reportages "
                    "spéciaux, nous nous efforçons de fournir une couverture équilibrée et approfondie pour "
                    "informer notre public.")),
                E("Interviews", image="pscreative/interview.webp", texte=(
                    "Nous proposons des interviews exclusives avec des personnalités influentes de la culture, "
                    "du divertissement, de la politique et plus encore. À travers nos interviews, nous donnons "
                    "la parole à ceux qui façonnent l'avenir de l'Afrique et inspirons notre public avec leurs "
                    "histoires et leurs idées.")),
            ]),
            S("video", "Nos émissions", "Découvrez AFRIJEUNE+ en vidéo", fond_alterne=True, elements=[
                E("AfriJeune+ en 3 mots", "AFRIJEUNE +", lien="https://www.youtube.com/watch?v=bkJFiy0ncQM"),
            ]),
        ],
    },
]


def G(libelle, type="multiple", obligatoire=False, aide="", icone="", options=()):
    return {"libelle": libelle, "type": type, "obligatoire": obligatoire, "aide": aide, "icone": icone,
            "options": list(options)}


def O(libelle, prix=None, description=""):
    return {"libelle": libelle, "prix": prix, "description": description}


# Offres d'EXEMPLE (prix indicatifs à remplacer dans l'admin).
OFFRES = [
    {
        "entreprise": "pscreative", "titre": "Couverture de mariage", "mise_en_avant": True,
        "image": "pscreative/shootingmariage.webp", "prix_a_partir_de": 150000,
        "resume": "Photo et vidéo de votre grand jour, de la préparation à la soirée.",
        "description": (
            "De la cérémonie à la réception, nous documentons chaque instant de bonheur, d'émotion et "
            "d'amour, avec une approche discrète et artistique pour des souvenirs intemporels.\n\n"
            "Composez votre couverture en cochant le matériel, la tenue de l'équipe et la durée qui vous "
            "conviennent : un membre de l'équipe vous rappelle pour finaliser le devis."),
        "galerie": ["pscreative/shootongmariage2.webp", "pscreative/shootingmariage.webp"],
        "groupes": [
            G("Matériel souhaité", aide="Cochez tout ce qui vous intéresse.", icone="camera", options=[
                O("Drone (prises de vue aériennes)", 50000),
                O("Second cadreur", 30000),
                O("Éclairage studio", 20000),
                O("Album photo imprimé", 40000),
            ]),
            G("Tenue de l'équipe", "unique", True, "Pour se fondre dans votre thème.", "shirt", options=[
                O("Classique (costume sombre)"), O("Traditionnelle"), O("Assortie à votre thème", 10000),
            ]),
            G("Durée de couverture", "unique", True, icone="clock", options=[
                O("Cérémonie uniquement"), O("Demi-journée", 25000), O("Journée complète", 50000),
            ]),
            G("Livrables vidéo", icone="film", options=[
                O("Film résumé (3 à 5 min)"), O("Film intégral", 30000), O("Teaser réseaux sociaux", 15000),
            ]),
        ],
    },
    {
        "entreprise": "pscreative", "titre": "Shooting photo", "mise_en_avant": True,
        "image": "pscreative/shooting1.webp", "prix_a_partir_de": 25000,
        "resume": "Beauté, anniversaire, grossesse, enfant ou portrait : une séance à votre image.",
        "description": (
            "Nos séances de shooting photo professionnelles sont conçues pour capturer vos moments les plus "
            "précieux avec une qualité exceptionnelle."),
        "galerie": ["pscreative/shooting2.webp", "pscreative/shootingrossesse.webp",
                    "pscreative/shootingenfant.webp", "pscreative/shootinhomm.webp"],
        "groupes": [
            G("Type de séance", "unique", True, icone="camera", options=[
                O("Beauté"), O("Anniversaire"), O("Grossesse"), O("Enfant"), O("Portrait homme"),
            ]),
            G("Lieu", "unique", True, icone="map-pin", options=[
                O("En studio"), O("En extérieur", 10000), O("À domicile", 15000),
            ]),
            G("Options", options=[
                O("Maquillage professionnel", 10000), O("Retouches avancées", 5000),
                O("Tirages photo", 15000), O("Mini-vidéo making-of", 10000),
            ]),
        ],
    },
    {
        "entreprise": "psdigital", "titre": "Gestion de pages réseaux sociaux", "mise_en_avant": True,
        "image": "pscreative/psdigit.webp", "prix_a_partir_de": 30000,
        "resume": "Création, animation et boost de vos pages pour développer votre audience.",
        "description": (
            "Nous créons et gérons des pages professionnelles sur les réseaux sociaux pour renforcer votre "
            "présence en ligne, de la conception de contenu à l'interaction avec les abonnés."),
        "groupes": [
            G("Plateformes", obligatoire=True, icone="hash", options=[
                O("Facebook"), O("Instagram"), O("TikTok"), O("YouTube"),
            ]),
            G("Formule", "unique", True, options=[
                O("Création des pages uniquement"), O("Gestion mensuelle", 20000),
            ]),
            G("Services complémentaires", options=[
                O("Sponsoring & boost", 15000), O("Visuels / infographies", 10000),
                O("Validation de compte", 25000), O("Filtre Snapchat", 15000),
            ]),
        ],
    },
    {
        "entreprise": "psdigital", "titre": "Site web sur mesure",
        "image": "pscreative/psdigit.webp",
        "resume": "Un site vitrine ou catalogue, rapide et adapté au mobile.",
        "description": "Développement web sur mesure, hébergement et maintenance.",
        "groupes": [
            G("Type de site", "unique", True, icone="code", options=[
                O("Site vitrine"), O("Site avec catalogue"), O("Boutique en ligne"),
            ]),
            G("Options", options=[
                O("Hébergement & nom de domaine"), O("Rédaction des contenus"), O("Maintenance mensuelle"),
            ]),
        ],
    },
    {
        "entreprise": "formation", "titre": "Session Class of Week",
        "image": "pscreative/creative.webp",
        "resume": "Une semaine intensive pour apprendre un métier de la création avec nos experts.",
        "description": (
            "Class of Week propose des formations spécialisées, dispensées par des professionnels "
            "expérimentés de chaque entreprise du groupe."),
        "groupes": [
            G("Filière", "unique", True, icone="graduation-cap", options=[
                O("Audiovisuel"), O("Digital & réseaux sociaux"), O("Musique & production"),
                O("Média & présentation TV"), O("Événementiel"), O("Infographie & création visuelle"),
            ]),
            G("Format", "unique", True, options=[O("En présentiel"), O("En ligne")]),
        ],
    },
    {
        "entreprise": "pszik", "titre": "Accompagnement musical", "mise_en_avant": True,
        "image": "pscreative/micro.webp",
        "resume": "De l'enregistrement à la distribution, un accompagnement complet pour votre projet.",
        "description": (
            "De la production à la distribution, nous offrons un accompagnement personnalisé pour aider les "
            "artistes à réussir dans le monde de la musique."),
        "groupes": [
            G("Services souhaités", obligatoire=True, icone="music", options=[
                O("Enregistrement"), O("Mixage & mastering"), O("Clip vidéo"), O("Distribution musicale"),
                O("Communication musicale"), O("Management d'artiste"),
            ]),
            G("Projet", "unique", options=[O("Single"), O("EP"), O("Album")]),
        ],
    },
    {
        "entreprise": "concours", "titre": "Candidature Miss Afrijeune",
        "image": "pscreative/missafri.webp",
        "resume": "Inscrivez-vous à la prochaine édition et choisissez votre mode d'audition.",
        "description": (
            "Jeunes femmes de tous les pays d'Afrique, sous réserve de répondre aux critères établis. "
            "Indiquez vos préférences : notre équipe vous rappelle pour fixer l'audition."),
        "groupes": [
            G("Mode d'audition", "unique", True, icone="video", options=[
                O("En présentiel à l'agence"), O("En ligne (hors de Yaoundé)"),
            ]),
            G("Je dispose déjà de", options=[
                O("Photos récentes"), O("Vidéo de présentation"), O("Liste de mes engagements sociaux"),
            ]),
        ],
    },
    {
        "entreprise": "afrijeune-plus", "titre": "Campagne sur AFRIJEUNE TV",
        "image": "pscreative/televise.webp",
        "resume": "Publicité, reportage ou interview : faites passer votre message à la jeunesse africaine.",
        "description": (
            "Nous offrons des services de communication télévisée pour transmettre vos messages à un large "
            "public à travers nos plateformes de diffusion."),
        "groupes": [
            G("Format", obligatoire=True, icone="tv", options=[
                O("Spot publicitaire"), O("Reportage"), O("Interview"), O("Partenariat de contenu"),
            ]),
            G("Durée de la campagne", "unique", options=[O("1 semaine"), O("1 mois"), O("3 mois")]),
        ],
    },
]
