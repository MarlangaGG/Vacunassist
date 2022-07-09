from flask import render_template, request, jsonify
from flask.helpers import make_response


def make_response(data, status):
    
    if request.path.startswith("/api/"):
        return jsonify(data), status
    else:  
        return render_template("error.html", **data), status


def bad_resquest(e):
    
    kwargs = {
        "error_name": "400 Bad request",
        "error_description": "Los datos ingresados no son correctos",
    }
    return make_response(kwargs, 400)

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return make_response(kwargs, 400)


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return make_response(kwargs, 401)

def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "El servidor encontró una condición inesperada que le impide completar la petición",
    }
    return make_response(kwargs, 500)


