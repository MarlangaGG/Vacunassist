from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)

def config_db(app):
    '''A partir de los modelos crea todas las tablas en la bd configurada'''
    @app.before_first_request
    def init_database():
        db.create_all()
    
    '''Borra la session de la bd'''
    @app.teardown_request
    def close_session(exeption=None):
        db.session.remove()

