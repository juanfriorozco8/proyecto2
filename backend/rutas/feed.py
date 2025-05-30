from flask import Blueprint, render_template, redirect, url_for, session as flask_session, jsonify
from ..utils.neo4j_driver import get_driver

feed_bp = Blueprint("feed", __name__)
driver = get_driver()

# Ruta /feed → página principal protegida
@feed_bp.route("/feed")
def feed():
    if "usuario" not in flask_session:
        return redirect("/login")
    return render_template("feed.html", usuario=flask_session["usuario"])

# Ruta /api/feed → devuelve cursos recomendados (simulado aquí)
@feed_bp.route("/api/feed", methods=["GET"])
def api_feed():
    if "usuario" not in flask_session:
        return jsonify({"error": "No autorizado"}), 401

    usuario = flask_session["usuario"]

    # Ejemplo simple: obtener cursos recomendados (simulado aquí)
    # En producción, aquí pondrías la consulta a Neo4j
    cursos = [
        {"titulo": "Python Básico", "duracion": "3h"},
        {"titulo": "Álgebra Lineal", "duracion": "4h"},
        {"titulo": "Historia de Roma", "duracion": "2h"},
    ]

    return jsonify({"cursos": cursos})
