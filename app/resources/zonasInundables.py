from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.zonasInundables import ZonasInundables
from sqlalchemy import update
from app.db import db
from app.models.configModule import ConfigModule
import os
from os.path import join, dirname, realpath
#import pandas as pd
from app.models.coordenadas import Coordenadas
import ast

def index():
    if not authenticated(session):
        abort(401)
    
    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    post_pagination = ZonasInundables.all_paginated(page, items_per_page, criterio_ordenacion)

    return render_template("zonasInundables/index.html", post_pagination=post_pagination)

def index_detalle(zona_id):
    if not authenticated(session):
        abort(401)
    zona = ZonasInundables.query.get(zona_id)
    coordenadas = zona.query.filter(Coordenadas.id_zona == zona_id)
    cant_puntos = zona.query.join(Coordenadas).where(zona.id == Coordenadas.id_zona).count()
    return render_template("zonasInundables/index_detalle.html",zona = zona, cant_puntos=cant_puntos, coordenadas=coordenadas)

def new():
    if not authenticated(session):
        abort(401)

    return render_template("zonasInundables/new.html")

def create():
    if not authenticated(session):
        abort(401)
     # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(os.getcwd(), 'app\\static\\' ,uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
        # save the file
    return redirect(url_for('zonasInundables_index'))

def parseCSV(filePath):
    # CVS Column Names
    col_names = ['nombre','coordenadas']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath,names=col_names, sep=',', header=None)

    # Loop through the Rows
    for i,row in csvData.iterrows():
        if not i == 0:
            zona = ZonasInundables(row['nombre'])
            db.session.add(zona)
            db.session.commit()
            zona = ZonasInundables.query.filter(ZonasInundables.nombre == row['nombre']).first()
            coordenadas_list = ast.literal_eval(row['coordenadas'])
            j = 1
            for element in coordenadas_list:
                element_str = ''.join(str(element))
                list = element_str.split('[')
                element_str = ''.join(list)
                list = element_str.split(']')
                element_str = ''.join(list)
                list = element_str.split(',')
                coordenada = Coordenadas(zona.id,list[0],list[1],j)
                j += 1
                db.session.add(coordenada)
                db.session.commit()
                
def eliminar(zona_id):
    if not authenticated(session):
        abort(401) 
    zona = ZonasInundables.query.get(zona_id)    
    return render_template("zonasInundables/eliminar.html", zona = zona) 

def delete(zona_id):
    if not authenticated(session):
        abort(401)
    zona = ZonasInundables.query.get(zona_id)
    db.session.delete(zona)
    db.session.commit()
    flash('Zona eliminada exitosamente')
    return redirect(url_for("zonasInundables_index"))

def resultados():
    if not authenticated(session):
        abort(401)

    config = ConfigModule.query.all()
    for element in config:
        items_per_page = element.cantidad_elementos_pagina
        criterio_ordenacion = element.criterio_ordenacion
    
    page = int(request.args.get('page', 1))
    post_pagination = ZonasInundables.all_paginated_filter(page, items_per_page, criterio_ordenacion, request.form["nombre"], request.form["flexRadioDeFilter"])

    return render_template("zonasInundables/resultados.html", post_pagination = post_pagination)          


