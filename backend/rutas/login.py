from flask import Blueprint, request, render_template, redirect, url_for, session as flask_session
from ..utils.neo4j_driver import get_driver

login_bp = Blueprint("login", __name__)
driver = get_driver()

@login_bp.route("/login", methods=["GET"])
def show_login():
    if "usuario" in flask_session:
        return redirect("/feed")
    return render_template("login.html")

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario", "").strip().lower()
    contrasena = data.get("contrasena", "").strip()

    if not usuario or not contrasena:
        return {"error": "Usuario y contraseña son requeridos"}, 400

    with driver.session(database="neo4j") as session:
        result = session.run(
            "MATCH (u:Usuario {usuario: $usuario, contrasena: $contrasena}) RETURN u",
            usuario=usuario,
            contrasena=contrasena
        )
        user = result.single()
        if not user:
            return {"error": "Credenciales incorrectas"}, 401

    flask_session["usuario"] = usuario
    return {"mensaje": "Inicio de sesión exitoso"}

@login_bp.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for("login.show_login"))
