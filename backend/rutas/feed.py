from flask import Blueprint, request, jsonify
from backend.utils.neo4j_driver import get_driver  


feed_bp = Blueprint('feed', __name__)
driver = get_driver()

# Endpoint: Obtener cursos recomendados para un usuario
@feed_bp.route('/feed', methods=['POST'])
def feed_usuario():
    data = request.get_json()
    username = data.get("usuario")

    with driver.session() as session:
        query = """
        MATCH (u:Usuario {usuario: $username})
        OPTIONAL MATCH (u)-[:INTERESADO_EN]->(cat:Categoria)<-[:PERTENECE_A]-(c:Curso)
        WHERE NOT (u)-[:INSCRITO_EN]->(c)
        WITH c, COUNT(*) AS coincidencias
        RETURN c.idCurso AS id, c.titulo AS titulo, c.categoria AS categoria, 
               c.dificultad AS dificultad, c.duracion AS duracion, c.foto AS foto,
               coincidencias
        ORDER BY coincidencias DESC
        LIMIT 10
        """
        resultados = session.run(query, username=username)

        cursos = []
        for record in resultados:
            cursos.append({
                "id": record["id"],
                "titulo": record["titulo"],
                "categoria": record["categoria"],
                "dificultad": record["dificultad"],
                "duracion": record["duracion"],
                "foto": record["foto"]
            })

    return jsonify(cursos)
