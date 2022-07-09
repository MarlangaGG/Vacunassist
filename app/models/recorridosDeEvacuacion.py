from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc
from app.models.coordenadas import Coordenadas

class RecorridosDeEvacuacion(db.Model):
    __tablename__ = "recorridos_de_evacuacion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True)
    descripcion = Column(String(100))
    coordenadas = Column(String(256))
    estado = Column(Boolean)
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, nombre=None, descripcion=None, estado=False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def all_paginated(page=1, per_page=5, criterio_ordenacion="nombre"):
        if criterio_ordenacion == "nombre":
            return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.nombre).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            return RecorridosDeEvacuacion.query.order_by(desc(RecorridosDeEvacuacion.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)

        if criterio_ordenacion == "fecha_desc":
            return RecorridosDeEvacuacion.query.order_by(desc(RecorridosDeEvacuacion.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)
    
    def all_paginated_filter(page=1, per_page=5, criterio_ordenacion="nombre", criterio_busqueda="", estado=""):
        if criterio_ordenacion == "nombre":
            if estado == "0":
                return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.nombre).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.nombre).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.nombre).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            if estado == "0":
                return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_desc":
            if estado == "0":
                return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 0).\
                paginate(page=page, per_page=per_page, error_out=False)
            else:
                if estado == "1":
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda)), RecorridosDeEvacuacion.estado == 1).\
                    paginate(page=page, per_page=per_page, error_out=False)
                else:
                    return RecorridosDeEvacuacion.query.order_by(RecorridosDeEvacuacion.estado).filter(RecorridosDeEvacuacion.nombre.like("%{}%".format(criterio_busqueda))).\
                    paginate(page=page, per_page=per_page, error_out=False)