from app.resources import usuario
from flask import redirect, render_template, request, url_for, abort, session, flash
from sqlalchemy.sql.functions import user
from app.models.user import User
import bcrypt
from app.models.usuario import Usuario
from app.models.misvacunas import Misvacunas
from app.db import db


def login():
    return render_template("auth/login.html")


def authenticate():
        
    params = request.form
    user = Usuario.query.filter(
        (Usuario.email == params["email"])
    ).first()
    if not user:
        flash("Usuario, clave o codigo F2A incorrecto.")
        return redirect(url_for("auth_login"))
    else:
       if params['password']== user.password:
           if int(params['codigo']) == int(user.codigo):
               
               if user.log == False:
                   
                   return render_template("auth/misvacunas.html",newuser = user)
               else:
                   session['user'] = user.email
                
                   return render_template("homepersona.html")
    flash("Usuario, clave o codigo F2A incorrecto.")
    return redirect(url_for("auth_login"))
    
    


def logout():
    del session["user"]
    session.clear()
    return redirect(url_for("auth_login"))

def signup():
    return render_template("auth/register.html")