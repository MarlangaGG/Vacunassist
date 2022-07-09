from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.puntosDeEncuentro import PuntosDeEncuentro
from sqlalchemy import update
from app.db import db
from app.models.configModule import ConfigModule

def index():
    

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    post_pagination = PuntosDeEncuentro.all_paginated(page, items_per_page, criterio_ordenacion)

    return render_template("puntosDeEncuentro/index.html", post_pagination=post_pagination)

def eliminar(punto_id):
    if not authenticated(session):
        abort(401)

    delete_punto = PuntosDeEncuentro.query.get(punto_id)
    db.session.delete(delete_punto)
    db.session.commit()
    flash('Punto eliminado')
    return redirect(url_for("puntosDeEncuentro_index"))

def new():
    if not authenticated(session):
        abort(401)

    return render_template("puntosDeEncuentro/new.html")

def create():
   if not authenticated(session):
        abort(401)
   new_punto = PuntosDeEncuentro(**request.form)
   db.session.add(new_punto)
   db.session.commit()    
   return redirect(url_for("puntosDeEncuentro_index"))

def modificar(punto_id):
    if not authenticated(session):
        abort(401)

    punto = PuntosDeEncuentro.query.get(punto_id)
    
    return render_template("puntosDeEncuentro/modificar.html", punto=punto)

def actualizar(punto_id):
    if not authenticated(session):
        abort(401)
    params = request.form
    punto = PuntosDeEncuentro.query.filter(PuntosDeEncuentro.id == punto_id).first()
    punto.nombre = params["nombre"] 
    punto.direccion = params["direccion"]
    punto.telefono = params["telefono"]
    punto.email = params["email"]  
    db.session.commit()
    flash('Punto editado exitosamente')
    return redirect(url_for("puntosDeEncuentro_index"))

def resultados():
    if not authenticated(session):
        abort(401)

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    puntos = PuntosDeEncuentro.all_paginated_filter(page, items_per_page, criterio_ordenacion, request.form["nombre"], request.form["flexRadioDeFilter"])
    return render_template("puntosDeEncuentro/resultados.html", puntos = puntos)