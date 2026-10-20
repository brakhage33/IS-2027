from . import health
from app import db

@health.route('/')
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "ok", "database": "ok"}, 200
    except Exception:
        return {"status": "error", "database": "error"}, 503
