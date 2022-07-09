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

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String(256))
    username = Column(String(30), unique=True)
    activo = Column(Boolean())
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, first_name=None, last_name=None, email=None, password=None, username=None, activo=1):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.username = username
        self.activo = activo
    
    @staticmethod
    def all_paginated(page=1, per_page=5, criterio_ordenacion="nombre"):
        if criterio_ordenacion == "nombre":
            return User.query.order_by(User.first_name).\
            paginate(page=page, per_page=per_page, error_out=False)
        
        if criterio_ordenacion == "fecha_asc":
            return User.query.order_by(User.create_at).\
            paginate(page=page, per_page=per_page, error_out=False)

        if criterio_ordenacion == "fecha_desc":
            return User.query.order_by(desc(User.create_at)).\
            paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def all_paginated_estado(page=1, per_page=5, criterio="activo"):
        if criterio == "activo":
            return User.query.filter(User.activo != 0).\
            paginate(page=page, per_page=per_page, error_out=False)
        
        if criterio == "bloqueado":
            return User.query.filter(User.activo == 0).\
            paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def has_permission(cls, user_id, permission):
        query = Permiso.query.join(RolTienePermiso).join(Rol).join(UsuarioTieneRol).join(User, User.id == UsuarioTieneRol.usuario_id).where(User.id == f"{user_id}")
        for element in query:
            if element.nombre == permission:
                return True
        return False
