from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.sql.elements import Null
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db
from app.models.configModule import ConfigModule
from sqlalchemy import update
import bcrypt

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    post_pagination = User.all_paginated(page, items_per_page, criterio_ordenacion)

    return render_template("user/index.html", post_pagination=post_pagination)


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
   if not authenticated(session):
        abort(401)
   params = request.form
   if params["password"] != params["password2"]:
       flash("La contraseñas no coinciden")
       return redirect(url_for("user_new"))
   userexist = User().query.filter(User.username == params["username"] or User.email == params["email"])
   if not userexist:
       flash("Ya existe ese nombre de usuario")
       return redirect(url_for("user_new"))
   password = params["password"]
   password = password.encode()
   sal = bcrypt.gensalt()
   password_hash = bcrypt.hashpw(password,sal)     
   new_user = User(params["first_name"],params["last_name"],params["email"],password_hash,params["username"])
   db.session.add(new_user)
   db.session.commit()    
   return redirect(url_for("user_index"))

def edit():
    if not authenticated(session):
        abort(401)
    myuser = User.query.filter(
        User.email == session["user"]
    ).first()
    return render_template("user/edit.html",myuser = myuser)

def update():
    
    if not authenticated(session):
        abort(401)
    
    params = request.form
    edit_user = User.query.filter(
       User.email == session["user"]
    ).first()
    edit_user.first_name = params["first_name"]
    edit_user.last_name = params["last_name"]
    if not edit_user.username == params["username"]:
        if exist_username(params["username"]):
            flash('Nombre de usuario existente')
            return redirect(url_for("user_edit"))
        edit_user.username = params["username"]        

    if not edit_user.email == params["email"]:
        if  exist_email(params["email"]):
            flash('Email existente. No se pueden actualizar los datos')
            return redirect(url_for("user_edit"))
        edit_user.email = params["email"]
        session["user"] = params["email"]
       
    db.session.commit()
    flash('Usuario editado exitosamente')
    return redirect(url_for("user_index"))

def exist_username(username):
    return User.query.filter(
        User.username == username
    ).first()

def exist_email(email):
    return User.query.filter(
        User.email == email
    ).first()


def eliminar(user_id):
    if not authenticated(session):
        abort(401)
    
    user = User.query.get(user_id)
    
    return render_template("user/eliminar.html", user = user)
    

def delete(user_id):
    if not authenticated(session):
        abort(401)
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente')
    return redirect(url_for("user_index"))
    

def activos():
    if not authenticated(session):
        abort(401)

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
            
    page = int(request.args.get('page', 1))
    post_pagination = User.all_paginated_estado(page, items_per_page, "activo")

    return render_template("user/index_activos.html", post_pagination=post_pagination)

def bloquear(user_id):
    if not authenticated(session):
        abort(401)
    
    block_user = User.query.get(user_id)
    block_user.activo = 0
    db.session.commit()
    flash('Usuario bloqueado exitosamente')
    return redirect(url_for("user_bloqueados"))

def bloqueados():
    if not authenticated(session):
        abort(401)

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
            
    page = int(request.args.get('page', 1))
    post_pagination = User.all_paginated_estado(page, items_per_page, "bloqueado")

    return render_template("user/index_bloqueados.html", post_pagination=post_pagination)

def activar(user_id):
    if not authenticated(session):
        abort(401)
    
    block_user = User.query.get(user_id)
    block_user.activo = 1
    db.session.commit()
    flash('Usuario activado exitosamente')
    return redirect(url_for("user_activos"))

def searchbyusername():
    if not authenticated(session):
        abort(401)
    
    params = request.form
    campo = params["campo"]
    search = "%{}%".format(campo)
    user = User.query.filter(
        User.username.like(search)
    ).all()
    
    if not user:
        flash("Nombre de usuario inexistente")
        return redirect(url_for("user_index"))

    return render_template("user/searchbyusername.html", users = user)




