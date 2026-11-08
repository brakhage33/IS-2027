#!/bin/bash

docker run -d --rm -p 9090:9999 --network pruebas \
  --name servidor_oche -v $(pwd):/app \
  python:3.7 python /app/tcp_servidor5_oche_readline.py