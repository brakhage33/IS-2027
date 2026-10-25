from flask import jsonify
from . import api
from app.models import Amigo

@api.route('/amigos', methods=['GET'])
def get_amigos():
    amigos = Amigo.query.all()
    return jsonify([{'id': a.id, 'name': a.name, 'longi': a.longi, 'lati': a.lati} for a in amigos])
