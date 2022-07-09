from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db

class ConfigModule(db.Model):
    __tablename__ = "configuraciones"
    id = Column(Integer, primary_key=True)
    cantidad_elementos_pagina = Column(Integer)
    criterio_ordenacion = Column(String(15))
    color_base = Column(String(15))
    color_texto_base = Column(String(15))
   
    def __init__(self, cantidad_elementos_pagina=None, criterio_ordenacion=None, color_base=None, color_texto_base=None):
        self.cantidad_elementos_pagina = cantidad_elementos_pagina
        self.criterio_ordenacion = criterio_ordenacion
        self.color_base = color_base
        self.color_texto_base = color_texto_base