from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import desc

class CategoriaDenuncia(db.Model):
    __tablename__ = "categoria_denuncia"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30))

    def __init__(self, nombre=None):
        self.nombre = nombre