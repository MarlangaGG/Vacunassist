import flask
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc
from app.models.coordenadas import Coordenadas


class ZonasInundables(db.Model):
    __tablename__ = "zonas_inundables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), unique=True)
    codigo_zona = Column(String(30), unique=True)
    estado = Column(Boolean)
    color_capa = Column(String(10))
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    coordenada = relationship("Coordenadas", cascade="all,delete", backref="ZonasInundables")

    def __init__(self, nombre=None, estado=False):
        self.nombre = nombre
        self.codigo_zona = None
        self.estado = estado
        self.color_capa = "#F52020"

    @staticmethod
    def all_paginated(page=1, per_page=5, criterio_ordenacion="nombre"):
        if criterio_ordenacion == "nombre":
            return ZonasInundables.query.order_by(ZonasInundables.nombre).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            return ZonasInundables.query.order_by(desc(ZonasInundables.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)

        if criterio_ordenacion == "fecha_desc":
            return ZonasInundables.query.order_by(desc(ZonasInundables.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)
      
    def all_paginated_filter(page=1, per_page=5, criterio_ordenacion="nombre", criterio_busqueda="", estado=""):
        if estado == "2":
            return ZonasInundables.query.order_by(ZonasInundables.nombre).filter(ZonasInundables.nombre.like("%{}%".format(criterio_busqueda))).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "nombre":
            return ZonasInundables.query.order_by(ZonasInundables.nombre).filter(ZonasInundables.estado == int(estado)).filter(ZonasInundables.nombre.like("%{}%".format(criterio_busqueda))).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_asc":
            return ZonasInundables.query.order_by(ZonasInundables.create_at).filter(ZonasInundables.estado == int(estado)).filter(ZonasInundables.nombre.like("%{}%".format(criterio_busqueda))).\
            paginate(page=page, per_page=per_page, error_out=False)
        if criterio_ordenacion == "fecha_desc":
            return ZonasInundables.query.order_by(desc(ZonasInundables.create_at)).filter(ZonasInundables.estado == int(estado)).filter(ZonasInundables.nombre.like("%{}%".format(criterio_busqueda))).\
            paginate(page=page, per_page=per_page, error_out=False)
    
    def as_dict(self):
        dict_zonas = {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        del dict_zonas['create_at']
        del dict_zonas['codigo_zona']
        del dict_zonas['estado']
        return dict_zonas

    def as_dict_pagination(self):
        dict_zonas = {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        coordenadas = Coordenadas.query.filter(Coordenadas.id_zona == self.id)
        dict_coordenadas = [coordenada.as_dict() for coordenada in coordenadas]
        coordenadas = {'coordenadas': dict_coordenadas}
        del dict_zonas['create_at']
        del dict_zonas['codigo_zona']
        del dict_zonas['estado']
        dict_zonas.update(coordenadas)
        return dict_zonas
