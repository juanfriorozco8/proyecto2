from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.neo4j_driver import get_driver
from algoritmo.recomendador import recomendar_cursos

feed_bp = Blueprint("feed", __name__)
driver = get_driver()

@feed_bp.route("/feed", methods=["GET"])
def show_feed():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("login.show_login"))

    cursos = recomendar_cursos(usuario)
    return render_template("feed.html", cursos=cursos, usuario=usuario)
