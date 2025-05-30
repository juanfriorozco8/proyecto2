from flask import Blueprint, request, render_template, redirect, url_for, session as flask_session
from ..utils.neo4j_driver import get_driver

login_bp = Blueprint("login", __name__)
driver = get_driver()

@login_bp.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    contrasena = data.get("contrasena")

    with driver.session() as neo4j_session:
        result = neo4j_session.run(
            "MATCH (u:Usuario {usuario: $usuario, contrasena: $contrasena}) RETURN u",
            usuario=usuario, contrasena=contrasena
        )
        user = result.single()

    if user:
        flask_session["usuario"] = usuario
        return {"mensaje": "Inicio de sesión exitoso"}
    else:
        return {"error": "Credenciales incorrectas"}, 401
