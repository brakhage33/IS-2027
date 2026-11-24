FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir wheel slixmpp==1.8.6
COPY . /app
CMD ["python3", "bot.py"]
Bash
docker build -t xmpp-bot ./bot
docker run -d --name xmpp-bot --network pruebas -e CLAVEBOT=tu_clave xmpp-bot
docker logs -f xmpp-bot
