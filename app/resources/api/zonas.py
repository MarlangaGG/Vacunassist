from flask import jsonify, Blueprint
from sqlalchemy.sql.traversals import NO_CACHE
from app.models.zonasInundables import ZonasInundables
from app.models.configModule import ConfigModule
from app.models.coordenadas import Coordenadas
from flask import request, session, abort
from app.helpers.auth import authenticated

zona_api = Blueprint("zona", __name__, url_prefix="/zonas-inundables/<int:id>")
zonas_api = Blueprint("zonas", __name__, url_prefix="/zonas-inundables/")

@zonas_api.get("/")
def index():
    if not authenticated(session):
        abort(401)
    config = ConfigModule.query.get(1)
    items_per_page = config.cantidad_elementos_pagina
    criterio_ordenacion = config.criterio_ordenacion

    page = int(request.args.get('page', 1))
    post_pagination = ZonasInundables.all_paginated(page, items_per_page, criterio_ordenacion) 
    
    zonas_query = post_pagination.items
    zonas_dict = [zona.as_dict_pagination() for zona in zonas_query]
    page_dict = [{'page': page, 'total':post_pagination.total}]
    zonas_dict.extend(page_dict)

    return jsonify(zona=zonas_dict)

@zona_api.get("/")
def show_zona(id):
    if not authenticated(session):
        abort(401)
    zonas_query = ZonasInundables.query.get(id)
    coordenadas_query = Coordenadas.query.filter(Coordenadas.id_zona == zonas_query.id)
    zonas_dict = [zonas_query.as_dict()] 
    coordenadas_dict = [ coordenada.as_dict() for coordenada in coordenadas_query ]
    zonas_dict.extend(coordenadas_dict) 

    return jsonify(zonas=zonas_dict)
