from flask import  request
from sqlalchemy.sql.expression import true
from app.db import db
from app.models.categoriaDenuncia import CategoriaDenuncia
from flask import abort
import re


def validarCreate(denuncia):
    
    validarDenuncia(denuncia)
    validarKeys(denuncia)
    validarTitulo(denuncia)
    return true

def validarDenuncia(denuncia):
    if denuncia == None:
        abort(400)
    if denuncia == {}:
        abort(400)
    if not (type(denuncia)) == dict:
        abort(400)
    return true

def noEsVacioyEsstr(dato):
    if not dato == '':
        if type(dato) == str:
            return True
    
    return abort(400)
    
def validarTitulo(denuncia):
    if noEsVacioyEsstr(denuncia["titulo"]):

        if len(denuncia["titulo"])<=30:
            
            return validarNombre(denuncia)
    
    return abort(400)

def validarNombre(denuncia):
    if noEsVacioyEsstr(denuncia["nombre_denunciante"]):
        if len(denuncia["nombre_denunciante"])<=50:
            return validarApellido(denuncia)
    
    return abort(400)

def validarApellido(denuncia):
    if noEsVacioyEsstr(denuncia["apellido_denunciante"]):
        if len(denuncia["apellido_denunciante"])<=50:
            return validarDescripcion(denuncia)
    
    return abort(400)

def validarDescripcion(denuncia):
    if noEsVacioyEsstr(denuncia["descripcion"]):
        if len(denuncia["descripcion"])<=256:
            return validarEmail(denuncia)
    
    return abort(400)

def validarEmail(denuncia):
    email = denuncia["email"]
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if re.match(expresion_regular, email) is not None:
        return validarTelefono(denuncia)
    return abort(400)

def validarTelefono(denuncia):
    regex = r"^([\d]){8,15}$"
    if re.match(regex, denuncia["telefono"]):
        return validarCategoria(denuncia)
    return abort(400)

def validarCategoria(denuncia):
    categoria = CategoriaDenuncia.query.filter(
        CategoriaDenuncia.id == denuncia["categoria"]
    ).first()
    if categoria:
        return True
    return abort(400)

def validarKeys(denuncia):
    listaKeys = ["apellido_denunciante", "categoria","coordenadas", "descripcion", "email","nombre_denunciante", "telefono","titulo"]
    theKeys = denuncia.keys()
    for elem in theKeys:
        if not elem in listaKeys:
            abort(400)
    
    return true

