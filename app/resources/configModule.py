from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.auth import authenticated
from app.db import db
from app.models.configModule import ConfigModule

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    return render_template("admin/config_module.html")

def update():
    if not authenticated(session):
        abort(401)
    elements_per_page = request.form.get('elements_per_page')
    criterio_ordenacion = request.form.get('criterio_ordenacion')
    base_color = request.form.get('input-color-base')
    text_color = request.form.get('input-color-text')
    
    config = ConfigModule.query.first()
    config.cantidad_elementos_pagina = elements_per_page
    config.criterio_ordenacion = criterio_ordenacion
    config.color_base = base_color
    config.color_texto_base = text_color
    db.session.commit()
    
    return redirect(url_for('home'))