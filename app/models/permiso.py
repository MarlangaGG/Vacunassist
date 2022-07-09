from typing import Tuple
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.traversals import COMPARE_FAILED
from app.db import db

class Permiso(db.Model):
    __tablename__ = "permiso"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30))

    def __init__(self, nombre=None):
        self.nombre = nombre