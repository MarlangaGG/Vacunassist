from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import true
from app.models.user import User
from app.models.denuncia import Denuncia
from app.models.seguimiento import Seguimiento
from app.helpers.auth import authenticated
from app.db import db
from app.models.configModule import ConfigModule
from sqlalchemy import update
from datetime import date, datetime
from sqlalchemy.sql.expression import desc
from app.models.categoriaDenuncia import CategoriaDenuncia
import bcrypt

def new():
    #if not authenticated(session):
        #abort(401)
    categorias = CategoriaDenuncia.query.all()
    return render_template("denuncia/new.html", categorias = categorias)

def create():
    params = request.form
    
    new_denuncia = Denuncia(params["titulo"], params["categoria"], params["descripcion"], False, params["apellido"], params["nombre"], params["telefono"], params["email"])
    if authenticated(session):
        new_denuncia.estado = 'En curso'
        flash("La deunucia ha sido registrada exitosamente")
    else:
        flash("La deunucia ha sido registrada exitosamente. Uno de nuestros operadores se comunicará brevemente")        
    db.session.add(new_denuncia)
    db.session.commit()
    
    return redirect(url_for("home"))

def index():
    if not authenticated(session):
        abort(401)
    
    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    
    post_pagination = Denuncia.all_paginated(page, items_per_page, criterio_ordenacion)
    
    
    return render_template("denuncia/index.html", post_pagination=post_pagination)

def show(denuncia_id):
    if not authenticated(session):
        abort(401)
    
    denuncia = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).filter(denuncia_id == Denuncia.id).first()
    
    return render_template("denuncia/show.html", denuncia = denuncia)

def edit(denuncia_id):
    if not authenticated(session):
        abort(401)
    
    denuncia = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).filter(denuncia_id == Denuncia.id).first()

    myuser = User.query.filter(
        User.email == session["user"]
    ).first()
    
    if not myuser.username == denuncia.asignado:
        flash("Usted no es el usuario asignado a la denuncia. No puede editarla")
        return redirect(url_for("denuncia_index"))
    categorias = CategoriaDenuncia.query.all()
    return render_template("denuncia/edit.html",denuncia = denuncia, categorias = categorias)
   
def update():
    if not authenticated(session):
        abort(401)
    
    params = request.form
    
    denuncia = Denuncia.query.filter(params["id"] == Denuncia.id).first()
    denuncia.titulo = params["titulo"]
    denuncia.categoria_id = params["categoria"]
    denuncia.nombre_denunciante = params["nombre"]
    denuncia.apellido_denunciante = params["apellido"]
    denuncia.telefono = params["telefono"]
    denuncia.email = params["email"]
    denuncia.descripcion = params["descripcion"]
    db.session.commit()
    flash('Denuncia editada exitosamente')
    return redirect(url_for("denuncia_show", denuncia_id = denuncia.id))

def eliminar(denuncia_id):
    if not authenticated(session):
        abort(401)
    denuncia = Denuncia.query.filter(denuncia_id == Denuncia.id).first()
        
    return render_template("denuncia/eliminar.html", denuncia = denuncia)

def delete(denuncia_id):
    if not authenticated(session):
        abort(401)
    denuncia = Denuncia.query.filter(denuncia_id == Denuncia.id).first()
    seguimientos = Seguimiento.query.filter(
         Seguimiento.denuncia_id == denuncia_id
    ).all()
    for seg in seguimientos:
        db.session.delete(seg)
    db.session.delete(denuncia)
    db.session.commit()
    flash('Denuncia eliminada exitosamente')
    return redirect(url_for("denuncia_index"))

def asignarme(denuncia_id):
    if not authenticated(session):
        abort(401)    
    denuncia = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).filter(denuncia_id == Denuncia.id).first()

    if not denuncia.asignado == None:
        flash("La denuncia ya se encuentra asignada a un usuario")
        return redirect(url_for("denuncia_index"))
    
    return render_template("denuncia/asignarme.html", denuncia = denuncia)

def confirmAsig(denuncia_id):
    if not authenticated(session):
        abort(401)
    
    denuncia = Denuncia.query.filter(denuncia_id == Denuncia.id).first()
    myuser = User.query.filter(
        User.email == session["user"]
    ).first()

    denuncia.asignado = myuser.username
    
    db.session.commit()
    flash("La denuncia ha sido asginada a usted")
    return redirect(url_for("denuncia_show", denuncia_id = denuncia.id))

def modificar_estado(denuncia_id):
    if not authenticated(session):
        abort(401)
    denuncia = Denuncia.query.filter(denuncia_id == Denuncia.id).first()
    myuser = User.query.filter(
        User.email == session["user"]
    ).first()
    
    if not myuser.username == denuncia.asignado:
        flash("Usted no es el usuario asignado a la denuncia. No puede modificar el estado")
        return redirect(url_for("denuncia_index"))
    if denuncia.estado == "Cerrada":
        flash("El estado de la denuncia es cerrada. No puede modificarse")
        return redirect(url_for("denuncia_show", denuncia_id = denuncia.id))
    return render_template("denuncia/modificar_estado.html",denuncia = denuncia)

def confirmar_estado():
    if not authenticated(session):
        abort(401)
    
    params = request.form
    denuncia = Denuncia.query.filter(params["id"] == Denuncia.id).first()
    denuncia.estado = params["estado"]
    if denuncia.estado == "Cerrada":
        denuncia.fecha_cierre = datetime.now()
    
    db.session.commit()
    flash('Se ha modificado el estado de la denuncia')
    return redirect(url_for("denuncia_show", denuncia_id = denuncia.id))

def incrementar_intentos(denuncia_id):
    if not authenticated(session):
        abort(401)
    
    denuncia = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).filter(denuncia_id == Denuncia.id).first()
    myuser = User.query.filter(
        User.email == session["user"]
    ).first()
    
    if not myuser.username == denuncia.asignado:
        flash("Usted no es el usuario asignado a la denuncia. No puede incrementar intentos")
        return redirect(url_for("denuncia_index"))
    
    if denuncia.estado == "Cerrada":
        flash("El estado de la denuncia es cerrada. No se puede incrementar intentos")
        return render_template("denuncia/show.html",denuncia = denuncia)
    
    denuncia.intentos = denuncia.intentos + 1
    if denuncia.intentos == 3:
        
        denuncia.fecha_cierre = datetime.now()
        denuncia.estado = "Cerrada"

        new_seguimiento = Seguimiento(myuser.username, "No fue posible contactar al denunciante", denuncia_id)
        db.session.add(new_seguimiento)
        

        flash("La denuncia ha alcanzado los 3 intentos. Se ha pasado a estado cerrada")
    else:
        flash("Se han incrementado los intentos")
    
    db.session.commit()
    return render_template("denuncia/show.html",denuncia = denuncia) 

def index_seguimientos(denuncia_id):
    if not authenticated(session):
        abort(401)
    
    seguimientos = Seguimiento.query.order_by(desc(Seguimiento.fecha_creacion)).filter(
        Seguimiento.denuncia_id == denuncia_id
    ).all()
    return render_template("denuncia/index_seguimientos.html", seguimientos = seguimientos, denuncia_id = denuncia_id)    
    
def new_seguimiento(denuncia_id):
    if not authenticated(session):
        abort(401)
    myuser = User.query.filter(
        User.email == session["user"]
    ).first()

    denuncia = Denuncia.query.filter(denuncia_id == Denuncia.id).first()
    users = User.query.all()

    if denuncia.estado == "Cerrada":
        flash("La denuncia ya se encuentra Cerrada. No puede agregar un seguimiento")
        return redirect(url_for("denuncia_index"))
    if not myuser.username == denuncia.asignado:
        flash("Usted no es el usuario asignado a la denuncia. No puede agregar un seguimiento")
        return redirect(url_for("denuncia_index"))
    return render_template("denuncia/new_seguimiento.html", denuncia_id = denuncia_id, users = users)    

def create_seguimiento():
    params = request.form
    autor = User.query.filter(
        User.email == session["user"]
    ).first()
    new_seguimiento = Seguimiento(params["username"], params["descripcion"], params["id"])
    db.session.add(new_seguimiento)
    db.session.commit()
    flash("El seguimiento ha sido registrada exitosamente")
    denuncia = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).filter(params["id"] == Denuncia.id).first()    
    return render_template("denuncia/show.html", denuncia = denuncia) 
    
def search():
    if not authenticated(session):
        abort(401)
        
    params = request.form
    titulo = "%{}%".format(params["titulo"])
    
    result = Denuncia.query.join(CategoriaDenuncia).where(Denuncia.categoria_id ==CategoriaDenuncia.id).order_by(desc(Denuncia.fecha_creacion)).filter(
        Denuncia.titulo.like(titulo)
    ).filter(
        Denuncia.estado == params["estado"]
    ).filter(
        Denuncia.fecha_creacion >= params["fechadesde"]
    ).filter(
        Denuncia.fecha_creacion <= params["fechahasta"]
    ).all()
    if not result:
        flash("No se obtuvieron resultados de la consulta")
        return redirect(url_for("denuncia_index"))
        
    return render_template("denuncia/searchresult.html", denuncias = result)