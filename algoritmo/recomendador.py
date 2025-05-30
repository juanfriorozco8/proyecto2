from algoritmo.utilidades_grafo import get_driver

import json

def cargar_pesos():
    with open("relaciones_interacciones/pesos_relaciones.json", "r", encoding="utf-8") as f:
        return json.load(f)

def recomendar_cursos(usuario):
    driver = get_driver()
    pesos = cargar_pesos()

    with driver.session() as session:
        query = """
        MATCH (u:Usuario {username: $usuario})
        OPTIONAL MATCH (u)-[:INTERESADO_EN]->(cat:Categoria)<-[:PERTENECE_A]-(c:Curso)
        OPTIONAL MATCH (u)-[:SIGUE_A]->(a:Autor)<-[:CREO]-(c)
        OPTIONAL MATCH (u)-[:INSCRITO_EN]->(ci:Curso)
        OPTIONAL MATCH (ci)-[sd:SIMILAR_DIFICULTAD]->(c)
        OPTIONAL MATCH (ci)-[dl:DURACION_SIMILAR]->(c)
        OPTIONAL MATCH (ci)-[ma:MISMO_AUTOR]->(c)
        OPTIONAL MATCH (u)-[like:DIO_LIKE]->(c)
        OPTIONAL MATCH (u)-[r:CALIFICO]->(c)

        WITH u, c, 
            COUNT(DISTINCT cat) * $peso_categoria +
            COUNT(DISTINCT a) * $peso_autor +
            COUNT(DISTINCT ci) * $peso_inscrito +
            COUNT(DISTINCT r) * $peso_rating +
            COUNT(DISTINCT sd) * $peso_sim_dif +
            COUNT(DISTINCT dl) * $peso_sim_dur +
            COUNT(DISTINCT ma) * $peso_mismo_autor +
            COUNT(DISTINCT like) * $peso_like AS score
        WHERE NOT (u)-[:INSCRITO_EN]->(c)
        RETURN c.titulo AS titulo, c.duracion AS duracion, score
        ORDER BY score DESC
        LIMIT 5
        """
        result = session.run(query, {
            "usuario": usuario,
            "peso_categoria": pesos.get("PERTENECE_A", 1),
            "peso_autor": pesos.get("SIGUE_A", 1),
            "peso_inscrito": pesos.get("INSCRITO_EN", 2),
            "peso_rating": pesos.get("CALIFICO", 1),
            "peso_like": pesos.get("DIO_LIKE", 3),
            "peso_sim_dif": pesos.get("SIMILAR_DIFICULTAD", 2),
            "peso_sim_dur": pesos.get("DURACION_SIMILAR", 2),
            "peso_mismo_autor": pesos.get("MISMO_AUTOR", 2)
        })
        return [record.data() for record in result]
