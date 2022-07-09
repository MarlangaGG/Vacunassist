from flask import jsonify, Blueprint, request
from sqlalchemy.sql.expression import true
from app.db import db
from app.models.denuncia import Denuncia
from app.resources.validaciones.denuncia import validarCreate

denuncia_post = Blueprint("denuncias", __name__, url_prefix="/denuncias")

@denuncia_post.post("/")
def create():
   
    denuncia = request.get_json()
    
    if validarCreate(denuncia):
                      
            new_denuncia = Denuncia(**request.get_json())
            db.session.add(new_denuncia)
            db.session.commit()
           
    return jsonify(new_denuncia.as_dict(), 201)