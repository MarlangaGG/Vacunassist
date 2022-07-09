from re import U
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import query, relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy import Date

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30))
    apellido = Column(String(30))
    dni = Column(String(8))
    fecnac = Column(Date)
    telefono = Column(String(15))
    zona = Column(Integer)
    email = Column(String(30), unique=True)
    password = Column(String(256))
    codigo = Column(Integer)
    rol = Column(String(15))
    riesgo = Column(Boolean())
    log = Column(Boolean())
    create_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, nombre=None, apellido=None, dni=None, fecnac=None, telefono=None, zona=None, email=None, password = None, codigo=None, rol = 'persona', riesgo=None):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fecnac = fecnac
        self.telefono = telefono
        self.zona = zona
        self.email = email
        self.password = password
        self.rol = rol
        self.codigo = codigo
        self.riesgo = riesgo
        self.log = 0
        
    
