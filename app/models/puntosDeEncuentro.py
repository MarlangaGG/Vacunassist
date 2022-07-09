from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc

class PuntosDeEncuentro(db.Model):
    __tablename__ = "puntos_de_encuentro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True)
    direccion = Column(String(50))
    coordenadas = Column(String(30))
    estado = Column(Boolean)
    telefono = Column(String(30))
    email = Column(String(30), unique=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, nombre=None, direccion=None, coordenadas=None, estado=False, telefono=None, email=None):
        self.nombre = nombre
        self.direccion = direccion
        self.coordenadas = coordenadas
        self.estado = estado
        self.telefono = telefono
        self.email = email
    
    @staticmethod
    def all_paginated(page=1, per_page=5, criterio_ordenacion="nombre"):
        if criterio_ordenacion == "nombre":
            return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.nombre).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            return PuntosDeEncuentro.query.order_by(desc(PuntosDeEncuentro.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)

        if criterio_ordenacion == "fecha_desc":
            return PuntosDeEncuentro.query.order_by(desc(PuntosDeEncuentro.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)

    def all_paginated_filter(page=1, per_page=5, criterio_ordenacion="nombre", criterio_busqueda="", estado=""):
        if criterio_ordenacion == "nombre":
            if estado == "0":
                return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.nombre).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.nombre).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.nombre).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            if estado == "0":
                return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_desc":
            if estado == "0":
                return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda)), PuntosDeEncuentro.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.estado).filter(PuntosDeEncuentro.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)