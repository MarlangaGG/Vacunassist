from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from app.models.rolTienePermiso import RolTienePermiso

class Rol(db.Model):
    __tablename__ = "rol"
    id = Column(Integer, ForeignKey("rol_tiene_permiso.rol_id"), primary_key=True)
    nombre = Column(String(20))
    rolTienePermiso = relationship(RolTienePermiso)

    def __init__(self, nombre=None):
        self.nombre = nombre