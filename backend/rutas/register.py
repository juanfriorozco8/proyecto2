from flask import Blueprint, request, render_template, redirect, url_for, session as flask_session
from ..utils.neo4j_driver import get_driver

register_bp = Blueprint("register", __name__)
driver = get_driver()

@register_bp.route("/register", methods=["GET"])
def show_register():
    return render_template("register.html")

@register_bp.route("/api/register", methods=["POST"])
def register_user():
    data = request.json
    usuario = data.get("usuario")
    contrasena = data.get("contrasena")
    correo = data.get("correo")
    intereses = data.get("intereses", [])

    with driver.session() as neo4j_session:
        neo4j_session.run(
            """
            CREATE (u:Usuario {usuario: $usuario, contrasena: $contrasena, correo: $correo})
            """, usuario=usuario, contrasena=contrasena, correo=correo
        )

        for interes in intereses:
            neo4j_session.run(
                """
                MATCH (u:Usuario {usuario: $usuario}), (c:Categoria {nombre: $interes})
                CREATE (u)-[:INTERESADO_EN]->(c)
                """, usuario=usuario, interes=interes
            )

    return {"mensaje": "Usuario registrado correctamente"}


