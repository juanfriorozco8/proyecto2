from neo4j import GraphDatabase
import json

# Conexión
driver = GraphDatabase.driver("neo4j+s://<tu_uri>", auth=("neo4j", "<tu_password>"))

# Cargar pesos
with open("relaciones_interacciones/pesos_relaciones.json") as f:
    PESOS = json.load(f)

def registrar_like(usuario_id, curso_id):
    with driver.session() as session:
        session.run("""
            MATCH (u:Usuario {id: $usuario_id}), (c:Curso {idCurso: $curso_id})
            MERGE (u)-[r:LIKE]->(c)
            SET r.peso = $peso
        """, usuario_id=usuario_id, curso_id=curso_id, peso=PESOS["CURSO_LIKEADO"])

def registrar_inscripcion(usuario_id, curso_id):
    with driver.session() as session:
        session.run("""
            MATCH (u:Usuario {id: $usuario_id}), (c:Curso {idCurso: $curso_id})
            MERGE (u)-[r:INSCRITO]->(c)
            SET r.peso = $peso
        """, usuario_id=usuario_id, curso_id=curso_id, peso=PESOS["CURSO_INSCRITO"])

# Agrega más funciones según la interacción

driver.close()
