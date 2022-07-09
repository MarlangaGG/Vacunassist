from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.sql.elements import Null
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db
from app.models.configModule import ConfigModule
from sqlalchemy import update
import bcrypt
from app.models.usuario import Usuario
from app.models.misvacunas import Misvacunas
from app.models.turno import Turno
from app.models.solicitud import Solicitud
import random
import datetime



def validardni(dni):
    if dni > 3000000:
        if dni < 90000000: 
            return True
    return False  


def create():
   
   params = request.form

   if params["dni"] == '1111111':
       flash("El DNI ingresado no es válido por RENAPER")
       return redirect(url_for("auth_signup"))
   
   if not validardni(int(params["dni"])):
       flash("El DNI ingresado no es válido")
       return redirect(url_for("auth_signup"))
   existdni = Usuario.query.filter(Usuario.dni == params["dni"]).first()
   
   if not existdni == None:
        flash('El DNI ingresado ya se encuentre registrado en el sistema')
        return redirect(url_for("auth_signup"))

   if params["password"] != params["password2"]:
       flash("Las contraseñas no coinciden")
       return redirect(url_for("auth_signup"))
   
   existuser = Usuario.query.filter(Usuario.email == params["email"]).first()
   
   if not existuser == None:
        flash('El email ingresado ya se encuentre registrado en el sistema')
        return redirect(url_for("auth_signup"))
 
  
   codigo = random.randint(1000,9999)
   
   newuser = Usuario(params["nombre"],params["apellido"],params["dni"],params["fechanac"],params["telefono"],params["zona"],params["email"],params["password"],codigo)
   db.session.add(newuser)
   db.session.commit()
   flash(f"El usuario ha sido creado exitosamente. Su código de acceso es {codigo}")    
   return redirect(url_for("home"))

def darturnogripe(newuser):
    ahora = datetime.datetime.utcnow()
    dias = ((ahora.date())-newuser.fecnac).days
    #si es mayor de 60 años
    if dias > 21900:
        #turno a los 3 meses
        fechag =  ahora + datetime.timedelta(days=90)
    else:
        #turno a los 6 meses
        fechag =  ahora + datetime.timedelta(days=180)
    
    fechag = fechag.date()
    hora = random.randint(8, 16)
    turnog = Turno(newuser.email,"Antigripal",fechag,hora, newuser.zona)
    db.session.add(turnog)


def darturnocovid(newuser):
    ahora = datetime.datetime.utcnow()
    dias = ((ahora.date())-newuser.fecnac).days
    #si es mayor a 18 años
    if dias > 6570:
        #si es mayor a 60 años
        if dias > 21900:
            #se da turno a 7 dias
            fechag =  ahora + datetime.timedelta(days=7)
            fechag = fechag.date()
            hora = random.randint(8, 16)
            turnoc = Turno(newuser.email,"Covid-19",fechag,hora, newuser.zona)
            db.session.add(turnoc)
        else:
            if newuser.riesgo == True:
                fechag =  ahora + datetime.timedelta(days=7)
                fechag = fechag.date()
                hora = random.randint(8, 16)
                turnoc = Turno(newuser.email,"Covid-19",fechag,hora, newuser.zona)
                db.session.add(turnoc)
            else:
                soli = Solicitud(newuser.email,"Covid-19")
                db.session.add(soli)



def registrarmisvacunas():
    params = request.form
    lista = []
    newuser = Usuario.query.filter(
       Usuario.email == params["email"]
    ).first()
    if params["riesgo"] == "si":        
        newuser.riesgo = True

    else:
        newuser.riesgo = False
    
    if params["fiebre"] == "si":
        newfiebre = Misvacunas(params["email"],"Fiebre amarilla",params["fechafiebre"])
        lista.append(newfiebre)
        db.session.add(newfiebre)
    if params["gripe"] == "si":
        newgripe = Misvacunas(params["email"],"Antigripal",params["fechagripe"])
        lista.append(newgripe)
        db.session.add(newgripe)
    else:
        darturnogripe(newuser)
                

    if params["covid"] == "si":
        newcovid = Misvacunas(params["email"],"Covid-19",params["fechacovid"])
        lista.append(newcovid)
        db.session.add(newcovid)
    else:
        darturnocovid(newuser)
        
    
    newuser.log = True
    session['user'] = newuser.email
    db.session.commit()

    return render_template("homepersona.html")
    


def edit():
    if not authenticated(session):
        abort(401)
    myuser = Usuario.query.filter(
        Usuario.email == session["user"]
    ).first()
    return render_template("usuario/edit.html",myuser = myuser)

def update():
    
    if not authenticated(session):
        abort(401)
    
    params = request.form
    edit_user = Usuario.query.filter(
       Usuario.email == session["user"]
    ).first()
    edit_user.nombre = params["nombre"]
    edit_user.apellido = params["apellido"]
    if params["dni"] == '1111111':
       flash("El DNI ingresado no es válido por RENAPER")
       return redirect(url_for("modificarperfil"))
   
    if not validardni(int(params["dni"])):
       flash("El DNI ingresado no es válido")
       return redirect(url_for("modificarperfil"))
    
    existdni = Usuario.query.filter(Usuario.dni == params["dni"]).first()

    if not existdni == None:
        flash('El DNI ingresado ya se encuentre registrado en el sistema')
        return redirect(url_for("modificarperfil"))

    edit_user.dni = params["dni"]
    
    edit_user.telefono = params["telefono"]
    edit_user.zona = params["zona"]

       
    db.session.commit()
    flash('Usuario editado exitosamente')
    return render_template("homepersona.html")

def editpass():
    if not authenticated(session):
        abort(401)
    
    return render_template("usuario/modificarpass.html")

def updatepass():
    if not authenticated(session):
        abort(401)
    
    params = request.form
    edit_user = Usuario.query.filter(
       Usuario.email == session["user"]
    ).first()
    if params["anterior"] == edit_user.password:
        if params["password"] == params["password2"]:
            edit_user.password = params["password"]
            db.session.commit()
            flash('La contraseña ha sido modificada')
            return render_template("homepersona.html")
        else:
            flash("Las contraseñas no coinciden")
            return redirect(url_for("modificarpass"))
    else:
        flash("La contraseña actual es incorrecta")
        return redirect(url_for("modificarpass"))

def homepersona():
    return render_template("homepersona.html")

def misvacunas():
    if not authenticated(session):
        abort(401)
    
    vacunas = Misvacunas.query.filter(
       Misvacunas.email == session["user"]
    ).all()
    return render_template("usuario/indexvacunas.html", vacunas = vacunas)


def misturnos():
    if not authenticated(session):
        abort(401)
    
    turnos = Turno.query.filter(
       Turno.email == session["user"]
    ).all()
    return render_template("usuario/indexturnos.html", turnos = turnos)




        