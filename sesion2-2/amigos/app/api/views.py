from flask import jsonify
from . import api
from app.models import Amigo

@api.route('/amigos', methods=['GET'])
def get_amigos():
    amigos = Amigo.query.all()
    return jsonify([{'id': a.id, 'name': a.name, 'longi': a.longi, 'lati': a.lati, 'device': a.device} for a in amigos])

@api.route('/devices', methods=['GET'])
def get_devices():
    devices_query = Amigo.query.with_entities(Amigo.device).filter(
        Amigo.device.isnot(None), 
        Amigo.device != ''
    ).distinct().all()
    return jsonify([d[0] for d in devices_query])