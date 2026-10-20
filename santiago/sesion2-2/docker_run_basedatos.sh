#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "== Limpiando contenedores previos (si existen) =="
docker rm -f basedatos amigos nginx 2>/dev/null || true

echo "== Asegurando que existe la red 'pruebas' =="
docker network create pruebas 2>/dev/null || true

echo "== Levantando basedatos (MariaDB) =="
docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v "$(pwd)/amigos/basedatos:/var/lib/mysql" \
  --rm --network pruebas -d mariadb

echo "== Esperando a que MariaDB acepte conexiones =="
until docker exec basedatos mariadb -u amigosuser -pamigospass amigosdb -e "SELECT 1;" >/dev/null 2>&1; do
  sleep 1
  echo -n "."
done
echo " listo"

echo "== Construyendo imagen amigos:1.0 =="
docker build -t amigos:1.0 ./amigos

echo "== Levantando contenedor amigos (Flask + gunicorn) =="
docker run --name amigos \
   -e DEPLOYMENT_MODE=production \
   -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
   --rm -d --network pruebas amigos:1.0

echo "== Aplicando migraciones (crea la tabla 'amigos' si hace falta) =="
sleep 2
docker exec -e FLASK_APP=lanzar.py amigos flask db upgrade

echo "== Levantando nginx =="
docker run --rm -d --network pruebas --name nginx \
       -v "$(pwd)/amigos/sitios_nginx:/etc/nginx/conf.d" \
       -p 80:80 nginx

echo
echo "== Todo listo =="
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
echo
echo "Prueba en: http://$(hostname -I | awk '{print $1}')/html/amigos"
