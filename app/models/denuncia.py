from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc
from app.models.categoriaDenuncia import CategoriaDenuncia

class Denuncia(db.Model):
    __tablename__ = "denuncias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(30))
    categoria_id = Column(Integer, ForeignKey("categoria_denuncia.id"), primary_key=True)
    categoria = relationship(CategoriaDenuncia)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_cierre = Column(DateTime(timezone=True))
    descripcion = Column(String(256))
    coordenadas = Column(String(100))
    estado = Column(String(30))
    asignado = Column(String(30))
    apellido_denunciante = Column(String(50))
    nombre_denunciante = Column(String(50))
    telefono = Column(String(30))
    email = Column(String(30))
    intentos = Column(Integer)

    def __init__(self, titulo=None, categoria=None, descripcion=None, coordenadas=False, apellido_denunciante=None, nombre_denunciante=None, telefono=None, email=None):
        self.titulo = titulo
        self.categoria_id = categoria
        self.fecha_cierre = None
        self.descripcion = descripcion
        self.coordenadas = coordenadas
        self.estado = "Sin confirmar"
        self.asignado = None
        self.apellido_denunciante = apellido_denunciante
        self.nombre_denunciante = nombre_denunciante
        self.telefono = telefono
        self.email = email
        self.intentos = 0
    
    def all_paginated(page=1, per_page=5, criterio_ordenacion="titulo"):
        return Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).order_by(desc(Denuncia.fecha_creacion)).\
        paginate(page=page, per_page=per_page, error_out=False)
    
    def as_dict(self):
        return {attr.name: getattr(self,attr.name) for attr in self.__table__.columns}
    
    
    

