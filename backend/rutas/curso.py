from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.neo4j_driver import get_driver

curso_bp = Blueprint("curso", __name__)
driver = get_driver()

@curso_bp.route("/curso/<idCurso>", methods=["GET"])
def ver_curso(idCurso):
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("login.show_login"))

    with driver.session() as neo4j_session:
        result = neo4j_session.run(
            """
            MATCH (c:Curso {idCurso: $idCurso})-[:CREADO_POR]->(a:Autor)
            RETURN c, a
            """, idCurso=idCurso
        )
        record = result.single()
        if not record:
            return "Curso no encontrado", 404

        curso = record["c"]
        autor = record["a"]

    return render_template("curso.html", curso=curso, autor=autor, usuario=usuario)
