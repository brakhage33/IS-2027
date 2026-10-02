#!/bin/bash
docker run -d --rm --name hola-flask \
    --network pruebas gunicornflask:1.0
docker run --rm -d --network pruebas --name nginx -p 80:80 -p 81:81 \
           -v $(pwd)/html:/usr/share/nginx/html \
           -v $(pwd)/html2:/usr/share/nginx/html2 \
           -v $(pwd)/sitios_nginx:/etc/nginx/conf.d nginx
