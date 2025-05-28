from flask import Blueprint, request, jsonify
from backend.utils.neo4j_driver import get_driver 


curso_bp = Blueprint('curso', __name__)
driver = get_driver()

# Endpoint: Obtener detalles de un curso por ID
@curso_bp.route('/curso/<id_curso>', methods=['GET'])
def obtener_curso(id_curso):
    with driver.session() as session:
        query = """
        MATCH (c:Curso {idCurso: $id})
        OPTIONAL MATCH (c)<-[:CREO]-(a:Autor)
        RETURN c.titulo AS titulo, c.categoria AS categoria, c.duracion AS duracion,
               c.dificultad AS dificultad, c.contenido AS contenido, c.foto AS foto,
               a.nombre AS autor_nombre, a.bio AS autor_bio, a.foto AS autor_foto
        """
        result = session.run(query, id=id_curso)
        curso = result.single()

        if curso:
            return jsonify({
                "titulo": curso["titulo"],
                "categoria": curso["categoria"],
                "duracion": curso["duracion"],
                "dificultad": curso["dificultad"],
                "contenido": curso["contenido"],
                "foto": curso["foto"],
                "autor": {
                    "nombre": curso["autor_nombre"],
                    "bio": curso["autor_bio"],
                    "foto": curso["autor_foto"]
                }
            })
        else:
            return jsonify({"error": "Curso no encontrado"}), 404


# Endpoint: Inscribir a un usuario a un curso
@curso_bp.route('/inscribir', methods=['POST'])
def inscribir_usuario():
    data = request.get_json()
    username = data.get("usuario")
    curso_id = data.get("curso_id")

    with driver.session() as session:
        query = """
        MATCH (u:Usuario {usuario: $username})
        MATCH (c:Curso {idCurso: $curso_id})
        MERGE (u)-[:INSCRITO_EN]->(c)
        """
        session.run(query, username=username, curso_id=curso_id)

    return jsonify({"mensaje": "Inscripción exitosa"}), 200


# Endpoint: Dar like/dislike o rating a un curso
@curso_bp.route('/rating', methods=['POST'])
def calificar_curso():
    data = request.get_json()
    username = data.get("usuario")
    curso_id = data.get("curso_id")
    rating = data.get("rating")  # puede ser un número o texto (like/dislike)

    with driver.session() as session:
        query = """
        MATCH (u:Usuario {usuario: $username})
        MATCH (c:Curso {idCurso: $curso_id})
        MERGE (u)-[r:CALIFICO]->(c)
        SET r.valor = $rating
        """
        session.run(query, username=username, curso_id=curso_id, rating=rating)

    return jsonify({"mensaje": "Calificación registrada"}), 200
