#!/bin/bash
# Lanza 3 servidores broadcast en contenedores dentro de la red "pruebas"

docker network create pruebas

ID1=$(docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py)
ID2=$(docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py)
ID3=$(docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py)

echo "Servidores lanzados:"
for id in $ID1 $ID2 $ID3; do
    echo "ID: $id"
    docker inspect $id | grep IPAddress
done
