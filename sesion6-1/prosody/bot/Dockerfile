FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir wheel slixmpp==1.8.6
COPY . /app
CMD ["python3", "bot.py"]