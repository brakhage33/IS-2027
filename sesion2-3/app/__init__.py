from .metrics import metrics as metrics_blueprint
app.register_blueprint(metrics_blueprint)