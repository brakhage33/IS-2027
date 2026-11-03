from flask import Response
from app.metrics import metrics
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

http_requests_total = Counter(
    "amigos_http_requests_total",
    "Número total de peticiones HTTP recibidas por Amigos"
)

http_errors_total = Counter(
    "amigos_http_errors_total",
    "Número total de respuestas HTTP de error"
)

http_request_duration_seconds = Histogram(
    "amigos_http_request_duration_seconds",
    "Tiempo de respuesta de las peticiones HTTP en segundos"
)

@metrics.route("/metrics")
def metrics_endpoint():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )