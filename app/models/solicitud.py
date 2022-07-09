from re import U
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import query, relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from app.models.usuarioTieneRol import UsuarioTieneRol
from app.models.rol import Rol
from app.models.rolTienePermiso import RolTienePermiso
from app.models.permiso import Permiso
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy import Date

class Solicitud(db.Model):
    __tablename__ = "solicitudes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(30))
    tipovacuna = Column(String(30))
    
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, email=None, tipovacuna=None):
        self.email = email
        self.tipovacuna = tipovacuna
        
        
