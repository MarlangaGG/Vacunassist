from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc
from app.models.denuncia import Denuncia

class Seguimiento(db.Model):
    __tablename__ = "seguimientos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    autor = Column(String(30))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    descripcion = Column(String(256))
    denuncia_id = Column(Integer, ForeignKey("denuncias.id"), primary_key=True)
    denuncia = relationship(Denuncia)

    def __init__(self, autor=None, descripcion=None, denuncia_id = None):
        self.autor = autor
        self.descripcion = descripcion
        self.denuncia_id = denuncia_id
        