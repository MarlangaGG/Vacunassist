from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from app.resources import user
from app.resources import auth
from app.resources import configModule
from app.resources import puntosDeEncuentro
from app.helpers import handler
from app.helpers import auth as helper_auth
import logging
from app.resources import denuncia
from app.resources.api.denuncia import denuncia_post
from app.resources import zonasInundables
from app.resources.api.zonas import zona_api
from app.resources.api.zonas import zonas_api
from app.resources import recorridosDeEvacuacion
from app.resources import home
from app.resources import usuario



logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Upload folder
    UPLOAD_FOLDER = 'static/files'
    app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_auth.check)

    # Autenticación
                    #navegador url   /   indice    /    redirije (del resources)
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas usuarios Vacunassit
    app.add_url_rule("/datosPersonales", "auth_signup", auth.signup)
    app.add_url_rule("/registrarse", "usuario_registrarse", usuario.create, methods=["POST"])
    app.add_url_rule("/modificarPerfil", "modificarperfil", usuario.edit)
    app.add_url_rule("/modificarDatos", "modificardatos", usuario.update, methods=["POST"])
    app.add_url_rule("/modificarPassword", "modificarpass", usuario.editpass)
    app.add_url_rule("/updatePassword", "updatepass", usuario.updatepass, methods=["POST"])
    app.add_url_rule("/registrarMisVacunas", "registrarmisvacunas", usuario.registrarmisvacunas, methods=["POST"])
    app.add_url_rule("/homepersona", "homepersona", usuario.homepersona)
    app.add_url_rule("/misVacunas", "misvacunas", usuario.misvacunas)
    app.add_url_rule("/misTurnos", "misturnos", usuario.misturnos)
    
    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/editar", "user_edit", user.edit)
    app.add_url_rule("/usuarios/actualizar", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/eliminar/<int:user_id>", "user_eliminar", user.eliminar, methods=["GET"])
    app.add_url_rule("/usuarios/delete/<int:user_id>", "user_delete", user.delete, methods=["GET"])
    app.add_url_rule("/usuarios/activos", "user_activos", user.activos)
    app.add_url_rule("/usuarios/bloquear/<int:user_id>", "user_bloquear", user.bloquear, methods=["GET"])
    app.add_url_rule("/usuarios/bloqueados", "user_bloqueados", user.bloqueados)
    app.add_url_rule("/usuarios/activar/<int:user_id>", "user_activar", user.activar, methods=["GET"])
    app.add_url_rule("/usuarios/searchbyusername", "user_searchbyusername", user.searchbyusername, methods=["POST"])

    # Rutas del Admin
    app.add_url_rule("/admin/config_module","config_module_index", configModule.index)
    app.add_url_rule("/admin/config_module/config_update","config_module_update", configModule.update, methods=["POST"])

    #Rutas puntos de encuentro
    app.add_url_rule("/puntos", "puntosDeEncuentro_index", puntosDeEncuentro.index)
    app.add_url_rule("/puntos/eliminar/<int:punto_id>", "puntosDeEncuentro_eliminar", puntosDeEncuentro.eliminar)
    app.add_url_rule("/puntos/nuevo", "puntosDeEncuentro_new", puntosDeEncuentro.new)
    app.add_url_rule("/puntos", "puntosDeEncuentro_create", puntosDeEncuentro.create, methods=["POST"])
    app.add_url_rule("/puntos/modificar/<int:punto_id>", "puntosDeEncuentro_modificar", puntosDeEncuentro.modificar)
    app.add_url_rule("/puntos/actualizar/<int:punto_id>", "puntosDeEncuentro_actualizar" , puntosDeEncuentro.actualizar, methods=["POST"])
    app.add_url_rule("/puntos/resultados", "puntosDeEncuentro_resultados", puntosDeEncuentro.resultados, methods=["POST"])
    
    #Rutas denuncias
    app.add_url_rule("/denuncias/nueva", "denuncia_new", denuncia.new)
    app.add_url_rule("/denuncias/creada", "denuncia_create", denuncia.create, methods=["POST"])
    app.add_url_rule("/denuncias", "denuncia_index", denuncia.index)
    app.add_url_rule("/denuncias/ver/<int:denuncia_id>", "denuncia_show", denuncia.show, methods=["GET"])
    app.add_url_rule("/denuncias/editar/<int:denuncia_id>", "denuncia_edit", denuncia.edit, methods=["GET"])
    app.add_url_rule("/denuncias/actualizar", "denuncia_update", denuncia.update, methods=["POST"])
    app.add_url_rule("/denuncias/eliminar/<int:denuncia_id>", "denuncia_eliminar", denuncia.eliminar, methods=["GET"])
    app.add_url_rule("/denuncia/delete/<int:denuncia_id>", "denuncia_delete", denuncia.delete, methods=["GET"])
    app.add_url_rule("/denuncias/asignarme/<int:denuncia_id>", "denuncia_asignarme", denuncia.asignarme, methods=["GET"])
    app.add_url_rule("/denuncia/confirmAsig/<int:denuncia_id>", "denuncia_confirmAsig", denuncia.confirmAsig, methods=["GET"])
    app.add_url_rule("/denuncia/ModificarEstado/<int:denuncia_id>", "denuncia_modificar_estado", denuncia.modificar_estado, methods=["GET"])
    app.add_url_rule("/denuncias/confirmarEstado", "denuncia_confirmar_estado", denuncia.confirmar_estado, methods=["POST"])
    app.add_url_rule("/denuncia/IncrementarIntentos/<int:denuncia_id>", "denuncia_incrementar_intentos", denuncia.incrementar_intentos, methods=["GET"])
    app.add_url_rule("/denuncias/VerSeguimientos/<int:denuncia_id>", "denuncia_index_seguimientos", denuncia.index_seguimientos, methods=["GET"])
    app.add_url_rule("/denuncias/NuevoSeguimiento/<int:denuncia_id>", "denuncia_new_seguimiento", denuncia.new_seguimiento, methods=["GET"])
    app.add_url_rule("/denuncias/CrearSeguimiento", "denuncia_create_seguimiento", denuncia.create_seguimiento, methods=["POST"])
    app.add_url_rule("/denuncias/DenunciaBusqueda", "denuncia_search", denuncia.search, methods=["POST"])

    # Rutas de zonas inundables
    app.add_url_rule("/zonasInundables", "zonasInundables_index", zonasInundables.index)
    app.add_url_rule("/zonasInundables/detalle/<int:zona_id>", "zonasInundables_index_detalle", zonasInundables.index_detalle)
    app.add_url_rule("/zonasInundables/nuevo", "zonasInundables_new", zonasInundables.new)
    app.add_url_rule("/zonasInundables/create", "zonasInundables_create", zonasInundables.create, methods=["POST"])
    app.add_url_rule("/zonasInundables/eliminar/<int:zona_id>", "zonasInundables_eliminar", zonasInundables.eliminar, methods=["GET"])
    app.add_url_rule("/zonasInundables/delete/<int:zona_id>", "zonasInundables_delete", zonasInundables.delete, methods=["GET"])
    app.add_url_rule("/zonasInundables/resultados", "zonasInundables_resultados", zonasInundables.resultados, methods=["POST"])

    #Rutas para Recorridos de evacuacion
    app.add_url_rule("/recorridos", "recorridosDeEvacuacion_index", recorridosDeEvacuacion.index)
    app.add_url_rule("/recorridos/nuevo", "recorridosDeEvacuacion_new", recorridosDeEvacuacion.new)
    app.add_url_rule("/recorridos", "recorridosDeEvacuacion_create", recorridosDeEvacuacion.create, methods=["POST"])
    app.add_url_rule("/recorridos/eliminar/<int:recorrido_id>", "recorridosDeEvacuacion_eliminar", recorridosDeEvacuacion.eliminar)
    app.add_url_rule("/recorridos/modificar/<int:recorrido_id>", "recorridosDeEvacuacion_modificar", recorridosDeEvacuacion.modificar)
    app.add_url_rule("/recorridos/actualizar/<int:recorrido_id>", "recorridosDeEvacuacion_actualizar", recorridosDeEvacuacion.actualizar, methods=["POST"])
    app.add_url_rule("/recorridos/resultados", "recorridosDeEvacuacion_resultados", recorridosDeEvacuacion.resultados, methods=["POST"])
    app.add_url_rule("/recorridos/detalle/<int:recorrido_id>", "recorridosDeEvacuacion_detalle", recorridosDeEvacuacion.detalle)

    # Ruta del home
    app.add_url_rule("/", "home", home.index)

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    
    api.register_blueprint(denuncia_post)
    api.register_blueprint(zona_api)
    api.register_blueprint(zonas_api)
    app.register_blueprint(api)

    
    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(500, handler.internal_server_error)
    app.register_error_handler(400, handler.bad_resquest)

    # Retornar la instancia de app configurada
    return app
