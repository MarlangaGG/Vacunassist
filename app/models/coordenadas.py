from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db


class Coordenadas(db.Model):
    __tablename__ = "coordenadas"
    id_zona = Column(Integer, ForeignKey('zonas_inundables.id'), primary_key=True)
    latitud = Column(String(256))
    longitud = Column(String(256))
    punto_id = Column(Integer, primary_key=True)


    def __init__(self, id_zona=None ,latitud=None, longitud=None, punto_id=None):
        self.id_zona = id_zona
        self.latitud = latitud
        self.longitud = longitud
        self.punto_id = punto_id

    def as_dict(self):
        dict_coordenadas = {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}
        del dict_coordenadas['id_zona']
        del dict_coordenadas['punto_id']
        return dict_coordenadas
