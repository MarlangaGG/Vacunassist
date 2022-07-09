from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from app.models.rol import Rol
from sqlalchemy.orm import relationship

class UsuarioTieneRol(db.Model):
    __tablename__ = "usuario_tiene_rol"
    usuario_id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey("rol.id"), unique=True)
    rol = relationship(Rol)
    
    def __init__(self, usuario_id=0, rol_id=None):
        self.usuario_id = 0
        self.rol_id = rol_id
        
    
    