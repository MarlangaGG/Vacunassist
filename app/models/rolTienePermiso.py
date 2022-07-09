from re import T
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.orm import relationship
from app.models.permiso import Permiso

class RolTienePermiso(db.Model):
    __tablename__ = "rol_tiene_permiso"
    rol_id = Column(Integer, primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permiso.id"), primary_key=True)
    permiso = relationship(Permiso)


    def __init__(self, rol_id=None, permiso_id=None):
        self.rol_id = rol_id
        self.permiso_id = permiso_id