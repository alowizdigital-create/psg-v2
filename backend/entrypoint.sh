#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput -v0
# Premier démarrage : importe le contenu du premier site (ne fait rien si du contenu existe déjà).
if [ "${SEED_CONTENU:-1}" = "1" ]; then
  python manage.py seed_contenu
fi
exec "$@"
