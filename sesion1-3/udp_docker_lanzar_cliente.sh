#!/bin/bash
# Lanza el cliente broadcast en un contenedor de la red "pruebas"
# Uso: ./udp_docker_lanzar_cliente.sh <ip_broadcast>


IP_BROADCAST=$1

docker run -it --network pruebas -v $(pwd):/app python:3.7 python /app/udp_cliente6_broadcast.py $IP_BROADCAST 12345
