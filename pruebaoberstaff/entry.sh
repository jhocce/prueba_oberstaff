#!/bin/sh
echo "Generando claves RSA..."
python GenKeRsa.py
# Recoger archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
python manage.py makemigrations -
# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate 
# Ejecutar comando principal
echo "Iniciando aplicación..."
exec "$@"