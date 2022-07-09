from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.recorridosDeEvacuacion import RecorridosDeEvacuacion
from sqlalchemy import update
from app.db import db
from app.models.configModule import ConfigModule

def index():
    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    page = int(request.args.get('page', 1))
    recorridos = RecorridosDeEvacuacion.all_paginated(page, items_per_page, criterio_ordenacion)
    return render_template("recorridosDeEvacuacion/index.html", recorridos=recorridos)

def new():
    if not authenticated(session):
        abort(401)
    return render_template("recorridosDeEvacuacion/new.html")

def create():
    if not authenticated(session):
        abort(401)
    new_recorrido = RecorridosDeEvacuacion(**request.form)
    db.session.add(new_recorrido)
    db.session.commit()    
    return redirect(url_for("recorridosDeEvacuacion_index"))

def eliminar(recorrido_id):
    if not authenticated(session):
        abort(401)
    delete_recorrido = RecorridosDeEvacuacion.query.get(recorrido_id)
    db.session.delete(delete_recorrido)
    db.session.commit()
    flash("Recorrido borrado")
    return redirect(url_for("recorridosDeEvacuacion_index"))

def modificar(recorrido_id):
    if not authenticated(session):
        abort(401)

    recorrido = RecorridosDeEvacuacion.query.get(recorrido_id)
    
    return render_template("recorridosDeEvacuacion/modificar.html", recorrido=recorrido)

def actualizar(recorrido_id):
    if not authenticated(session):
        abort(401)
    params = request.form
    recorrido = RecorridosDeEvacuacion.query.filter(RecorridosDeEvacuacion.id == recorrido_id).first()
    recorrido.nombre = params["nombre"]   
    recorrido.descripcion = params["descripcion"]
    db.session.commit()
    flash('Recorrido editado exitosamente')
    return redirect(url_for("recorridosDeEvacuacion_index"))

def resultados():
    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    recorridos = RecorridosDeEvacuacion.all_paginated_filter(page, items_per_page, criterio_ordenacion, request.form["nombre"], request.form["flexRadioDeFilter"])

    return render_template("recorridosDeEvacuacion/resultados.html", recorridos = recorridos)

def detalle(recorrido_id):
    if not authenticated(session):
        abort(401)
    recorrido = RecorridosDeEvacuacion.query.get(recorrido_id)
    return render_template("recorridosDeEvacuacion/detalle.html", recorrido = recorrido)