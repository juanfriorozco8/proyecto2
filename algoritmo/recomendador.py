# algoritmo/recomendador.py

import json
from utilidades_grafo import Neo4jConnector

def cargar_pesos(path="relaciones_interacciones/pesos_relaciones.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def recomendar_cursos(connector, usuario_id):
    pesos = cargar_pesos()

    query = """
    MATCH (u:Usuario {id: $usuario_id})

    // Cursos por categoría de interés
    OPTIONAL MATCH (u)-[:INTERESADO_EN]->(cat:Categoria)<-[:PERTENECE_A]-(c1:Curso)
    WHERE NOT (u)-[:YA_TOMO]->(c1)
    WITH u, c1 AS curso, count(*) AS score_categoria

    // Cursos por autor que el usuario ya tomó
    OPTIONAL MATCH (u)-[:YA_TOMO]->(:Curso)-[:ES_DE]->(a:Autor)<-[:ES_DE]-(c2:Curso)
    WHERE NOT (u)-[:YA_TOMO]->(c2)
    WITH u, curso, score_categoria, c2 AS curso2, count(*) AS score_autor

    // Cursos con misma dificultad
    OPTIONAL MATCH (u)-[:YA_TOMO]->(prev:Curso), (curso3:Curso)
    WHERE prev.dificultad = curso3.dificultad AND NOT (u)-[:YA_TOMO]->(curso3)
    WITH u, curso, score_categoria, score_autor, curso3, count(*) AS score_dificultad

    // Cursos populares (más inscritos)
    OPTIONAL MATCH (curso4:Curso)<-[:INSCRITO_EN]-(:Usuario)
    WHERE NOT (u)-[:YA_TOMO]->(curso4)
    WITH u, curso, score_categoria, score_autor, score_dificultad, curso4, count(*) AS score_popularidad

    // Cursos con mayor rating
    OPTIONAL MATCH (curso5:Curso)<-[r:CALIFICO]-(:Usuario)
    WHERE NOT (u)-[:YA_TOMO]->(curso5)
    WITH u, curso, score_categoria, score_autor, score_dificultad, score_popularidad, curso5, avg(r.valor) AS score_rating

    // Similaridad por intereses
    OPTIONAL MATCH (u)-[:INTERESADO_EN]->(cat)<-[:INTERESADO_EN]-(similar:Usuario)-[:YA_TOMO]->(curso6:Curso)
    WHERE NOT (u)-[:YA_TOMO]->(curso6)
    WITH curso, curso2, curso3, curso4, curso5, curso6,
         score_categoria, score_autor, score_dificultad, score_popularidad, score_rating,
         count(*) AS score_similitud

    // Unir todos los cursos en un solo conjunto con COALESCE
    WITH collect(DISTINCT curso) + collect(DISTINCT curso2) + collect(DISTINCT curso3) +
         collect(DISTINCT curso4) + collect(DISTINCT curso5) + collect(DISTINCT curso6) AS todos

    UNWIND todos AS curso_recomendado
    WITH DISTINCT curso_recomendado
    OPTIONAL MATCH (curso_recomendado)<-[:PERTENECE_A]-(cat:Categoria)
    OPTIONAL MATCH (curso_recomendado)-[:ES_DE]->(a:Autor)
    OPTIONAL MATCH (curso_recomendado)<-[:CALIFICO]-(u)-[r:CALIFICO]->(curso_recomendado)
    OPTIONAL MATCH (curso_recomendado)<-[:INSCRITO_EN]-(:Usuario)

    WITH curso_recomendado,
         count { (curso_recomendado)<-[:PERTENECE_A]-(cat) } AS cat_score,
         count { (curso_recomendado)-[:ES_DE]->(a) } AS autor_score,
         count { (u)-[:YA_TOMO]->(:Curso {dificultad: curso_recomendado.dificultad}) } AS dificultad_score,
         count { (curso_recomendado)<-[:INSCRITO_EN]-(:Usuario) } AS popularidad_score,
         avg(r.valor) AS rating_score,
         count { (u)-[:INTERESADO_EN]->()<-[:INTERESADO_EN]-(similar:Usuario)-[:YA_TOMO]->(curso_recomendado) } AS similitud_score

    WITH curso_recomendado,
         cat_score * $peso_categoria +
         autor_score * $peso_autor +
         dificultad_score * $peso_dificultad +
         popularidad_score * $peso_popularidad +
         rating_score * $peso_rating +
         similitud_score * $peso_usuario_similar AS score_total

    RETURN curso_recomendado.titulo AS titulo, score_total
    ORDER BY score_total DESC
    LIMIT 5
    """

    params = {
        "usuario_id": usuario_id,
        "peso_categoria": pesos.get("categoria", 1),
        "peso_autor": pesos.get("autor", 1),
        "peso_dificultad": pesos.get("dificultad", 1),
        "peso_popularidad": pesos.get("popularidad", 1),
        "peso_rating": pesos.get("rating", 1),
        "peso_usuario_similar": pesos.get("usuario_similar", 1)
    }

    return connector.ejecutar_query(query, params)
