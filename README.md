# PS GROUP SARL — nouveau site (v2)

Nouveau site animé de PS GROUP SARL, avec **catalogues dynamiques** gérés depuis une **interface d'administration**.
Le premier site statique (dépôt `psg`) n'est pas modifié et continue de tourner.

- **Site public** (Next.js) : reprend le contenu et les menus du premier site (Accueil, À propos, Nos entreprises, Contact) avec un design animé, plus un **Catalogue**.
- **Admin** (Django, `/admin`) : connexion obligatoire. Les gestionnaires créent les offres de leur entreprise et suivent les demandes.
- **Demandes clients** : le visiteur coche les options qui l'intéressent (drone, tenue…), envoie sa demande. Elle est enregistrée avec tous ses choix et notifiée **au client (SMS)**, **à l'équipe de l'entreprise** et **au superadmin**.

```
backend/    Django 5 + Django REST Framework (admin, API, notifications)
frontend/   Next.js 16 + Motion (site public animé)
Caddyfile   reverse proxy + HTTPS automatique
docker-compose.yml
```

## Parcours d'une demande

1. Le client ouvre une offre du catalogue (ex. « Couverture de mariage »), coche ses options : le total estimé se met à jour en direct.
2. Il saisit nom, téléphone (+ e-mail, date, lieu, message facultatifs) et envoie.
3. Le serveur **revérifie** les options (appartenance à l'offre, choix obligatoires, choix unique) et **recalcule le total** à partir des prix en base. Les prix envoyés par le navigateur sont ignorés.
4. La demande est enregistrée avec une **copie figée** de chaque option cochée (libellé + prix), visible dans *Admin › Demandes clients*.
5. Notifications envoyées en arrière-plan et journalisées (*Admin › Journal des notifications*) :
   - **client** : SMS « … votre demande PSG-2026-0001 est bien reçue. Un membre de notre équipe vous appellera très bientôt. » (+ e-mail s'il a donné son adresse) ;
   - **équipe de l'entreprise** : SMS court + e-mail détaillé (choix, total, liens d'appel et WhatsApp), envoyés aux numéros/e-mails de l'entreprise et à ses gestionnaires ;
   - **superadmin** : même récapitulatif, pour toutes les entreprises (comptes superutilisateurs + contacts de supervision des *Réglages du site*).

   Un SMS ou un e-mail en échec ne fait jamais perdre la demande. On peut le relancer avec `python manage.py retry_notifications`.

## Utiliser l'admin

### Créer un gestionnaire (superadmin)
*Admin › Utilisateurs › Ajouter* : identifiant, nom, e-mail, mot de passe. Puis, sur la fiche :
- dans **Profil**, choisir **les entreprises gérées** et le **téléphone** qui recevra les SMS de demandes ;
- le compte est automatiquement « Statut équipe » + groupe **Gestionnaire**.

Un gestionnaire ne voit et ne modifie **que** les offres, la page et les demandes de ses entreprises. Un **superadmin** (case « Statut superutilisateur ») voit tout et reçoit toutes les demandes.

### Créer un catalogue
Un catalogue = l'ensemble des **offres** d'une entreprise. *Admin › Offres du catalogue › Ajouter* :
1. **L'offre** : entreprise, titre, résumé, description, case **Publiée** (décochée = brouillon invisible).
2. **Image et prix** : image principale (convertie automatiquement en WebP), prix « à partir de » (facultatif).
3. **Groupes d'options** (« Ajouter un objet Groupe d'options ») : une question posée au client, par ex. « Matériel souhaité ». Pour chaque groupe : type **plusieurs choix** ou **un seul choix**, **obligatoire** ou non.
4. Dans chaque groupe, les **options** : libellé, description, prix supplémentaire, photo, case **Disponible**. Glisser-déposer pour réordonner.
5. **Galerie photo** de l'offre.
6. **Enregistrer** : le site est mis à jour immédiatement.

Actions utiles dans la liste : **Dupliquer** une offre (pour partir d'un modèle), **Publier**, **Retirer du site**.

### Pages et réglages
- *Entreprises* : textes de la page de chaque entreprise, bannière, bandeau de contact, et ses blocs de contenu (galerie, cartes, personnes, vidéo…).
- *Sections de pages* (superadmin) : blocs de l'Accueil, de l'À propos et du Contact.
- **Blocs animés** (types de sections, utilisés sur la page PS Digital) :
  - *Bloc qui s'ouvre au défilement* : le **titre** s'affiche en très grand, coupé en deux ; en faisant défiler, un panneau s'ouvre entre les deux moitiés. Le **sur-titre** est le grand titre du panneau, le **texte** son sous-titre, le **bouton** s'affiche dessous. Les **éléments** donnent les mots animés du fond (ou une image : la première image d'élément remplace l'animation).
  - *Bandeau de mots défilants* : deux rangées de mots (un mot par élément) qui accélèrent et changent de sens avec le défilement.
  - *Panneaux d'images qui s'ouvrent au survol* : photos en noir et blanc côte à côte avec le titre à la verticale ; au survol, le panneau s'élargit, passe en couleur et montre son texte et un bouton « Découvrir » (vers le **lien** de l'élément). Sans élément, le bloc affiche les offres du catalogue de l'entreprise.
  - *Grille de logos en losanges* : tuiles blanches inclinées ; un élément = un logo. Saisissez le **nom d'un réseau** (Facebook, Instagram, TikTok, YouTube, WhatsApp, Snapchat, X, Telegram, Pinterest, Threads, Messenger, Twitch, Discord, Spotify, Google, Reddit, Behance, Bluesky) et son logo s'affiche tout seul ; sinon ajoutez une **image** (ex. logo d'un partenaire). Le **lien** est facultatif ; cochez **mis en avant** sur un logo pour le placer au centre de la grille.
  - *Texte géant qui défile* : le **titre** (ex. PS DIGITAL) en très grand sur deux rangées, l'une pleine, l'autre évidée, qui glissent en sens inverse quand on fait défiler la page. Le **sur-titre**, s'il est rempli, remplace le texte de la seconde rangée.
  - *Lecteur de chansons* (page PS ZIK) : **3 chansons au maximum**. Pour chaque chanson, ajoutez un élément : **titre** = nom de la chanson, **sous-titre** = artiste, **image** = pochette (facultative), **fichier audio** = la chanson (MP3 conseillé, 20 Mo maximum) — ou, à la place du fichier, un **lien Spotify** (open.spotify.com/track/…) dans « lien » : le lecteur Spotify officiel s'affiche. Les cartes sont dans le style Spotify, avec un fond de la couleur de la pochette. Une seule chanson joue à la fois ; tant qu'aucune chanson n'est ajoutée, 3 cartes « Bientôt disponible » s'affichent.
  - *Liste interactive* : grands titres numérotés ; au survol, la ligne se colore et le détail (texte de l'élément) s'affiche à droite (sous la ligne sur mobile).
- Le bloc *Offres du catalogue mises en avant* (accueil) s'affiche en **panneaux d'images qui s'ouvrent au survol** (8 offres au plus, celles cochées « mise en avant », sinon toutes) : photo de l'offre, entreprise, prix et bouton « Composer ».
- Sur une page d'entreprise, la grille automatique « Demander un devis » (offres du catalogue) n'est pas affichée si la page contient déjà un bloc *Panneaux d'images* ou *Offres*.
- *Avis clients* : un avis = nom, qualité/ville, texte, note sur 5, photo facultative. Choisissez une **offre** (il s'affiche sous cette offre) ou seulement une **entreprise** (il s'affiche sous toutes ses offres), et cochez **Afficher sur la page d'accueil** pour le montrer aussi sur l'accueil. Pour afficher le bouton **« Confirmer l'avis »** (qui ouvre WhatsApp vers le client avec un message déjà rédigé), saisissez le **WhatsApp du client** et cochez **l'accord du client** : sans accord, pas de bouton. Le numéro n'apparaît jamais dans le code de la page, seulement dans la redirection. Un avis décoché « Publié » est masqué. Sans avis publié, les sections n'apparaissent pas.
- *Diaporama d'ouverture d'une entreprise* : sur la fiche *Entreprises*, bloc « Diaporama d'ouverture » : ajoutez de grandes images (elles défilent en plein écran à l'ouverture de la page, comme à l'accueil). Les photos s'affichent seules (sans texte) ; le champ **Logo** de la fiche pose le logo en haut à droite. Sans image, la page garde son bandeau classique. Pour Miss Afrijeune, `python manage.py diaporama_entreprises` ajoute le diaporama de départ.
- *Style du diaporama d'ouverture* (fiche *Entreprises*) : « Photos seules » (comme Miss Afrijeune) ou « Grand titre animé qui vibre comme de la musique » (comme PS ZIK : titre avec effet glitch rouge/bleu au rythme, sous-titre espacé, égaliseur animé). Renseignez le **grand titre** (ex. PS ZIK) et le **sous-titre** (ex. Production musicale).
- *Diaporama d'accueil*, *Réglages du site* : coordonnées, WhatsApp, **liens réseaux sociaux** (vides au départ : les icônes n'apparaissent qu'une fois renseignées), texte du SMS de confirmation, contacts de supervision.
- *Demandes clients* : statut (nouvelle → client contacté → confirmée…), notes internes, export PDF des demandes sélectionnées.

## Lancer en local (développement)

Prérequis : Python 3.12+, Node.js 22+.

```bash
cd backend
python -m venv ../.venv && . ../.venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
export DJANGO_DEBUG=1
python manage.py migrate
python manage.py seed_contenu        # importe le contenu du premier site + offres d'exemple
python manage.py createsuperuser
python manage.py runserver 8000
```

```bash
cd frontend
npm install
npm run build && npm start           # http://localhost:3000 (admin : http://localhost:3000/admin)
```

`npm run dev` fonctionne aussi. En développement, les SMS et e-mails sont **affichés dans le terminal de Django** au lieu d'être envoyés.

Tests du backend : `cd backend && python -m pytest`.

## Mise en production (Docker)

Sur un serveur (VPS) avec Docker, et un nom de domaine (ex. `nouveau.psgroupsarl.com`) qui pointe vers lui :

```bash
cp .env.example .env      # compléter : SITE_DOMAIN, secrets, SMS, SMTP
docker compose up -d --build
docker compose exec backend python manage.py createsuperuser
```

Au premier démarrage, la base est créée et le contenu du premier site est importé automatiquement (`SEED_CONTENU=0` pour désactiver). Caddy obtient le certificat HTTPS tout seul. Le site actuel peut rester en ligne sur son domaine jusqu'au basculement.

Sauvegardes à prévoir : le volume `pgdata` (base) et le volume `media` (images).

### Serveur géré par Dokploy (Traefik)

Si Traefik (Dokploy) occupe déjà les ports 80/443, ne lancez pas Caddy :

```bash
cp .env.example .env      # SITE_DOMAIN=psgroupsarl.com, secrets, SMS…
docker compose -f docker-compose.yml -f docker-compose.vps.yml -p psgv2 up -d --build
sudo cp deploy/traefik-psg-v2.yml /etc/dokploy/traefik/dynamic/psg-v2.yml   # psgroupsarl.com (+ www, v2 redirigés)
docker compose -p psgv2 exec backend python manage.py createsuperuser
```

Mise à jour : `git pull` puis la même commande `up -d --build`.

## SMS

Le fournisseur se choisit dans `.env` (`SMS_PROVIDER`) :
- `console` (défaut) : rien n'est envoyé, le SMS est écrit dans les logs. Pratique en attendant le fournisseur.
- `techsoft` : **Techsoft SMS** (Cameroun). Renseigner `TECHSOFT_API_TOKEN` et `SMS_SENDER_ID` (nom d'expéditeur validé chez Techsoft, 11 caractères max).
  Tester depuis le serveur : `docker compose exec backend python manage.py test_sms 6XXXXXXXX`
- `twilio` : renseigner `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`.
- `http` : agrégateur local (MTN/Orange/Nexttel via un prestataire). Adapter le format de la requête dans `backend/notifications/sms.py` (`HttpProvider`) à l'API du prestataire retenu.

⚠️ Au Cameroun, l'opérateur **MTN impose l'enregistrement préalable du nom d'expéditeur** (ex. « PSGROUP »). Comptez plusieurs semaines et vérifiez les conditions avec le fournisseur choisi.

## À compléter par l'équipe

- **Prix et options des offres** : les 8 offres importées sont des **exemples**, avec des prix indicatifs à remplacer.
- Liens des réseaux sociaux du groupe, vrai logo, photos du diaporama.
- Fournisseur SMS et compte SMTP (e-mails).
- Les images de la page Formation (lauréats) et de PSG ZIK (artistes) sont reprises du premier site : vérifier les droits d'utilisation.
