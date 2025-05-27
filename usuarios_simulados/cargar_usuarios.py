from neo4j import GraphDatabase
import json

URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def cargar_usuarios(tx, usuario):
    tx.run("""
        MERGE (u:Usuario {usuario: $usuario, correo: $correo, contraseña: $contraseña})
    """, **usuario)
    
    for categoria in usuario["intereses_iniciales"]:
        tx.run("""
            MATCH (u:Usuario {usuario: $usuario})
            MERGE (c:Categoria {nombre: $categoria})
            MERGE (u)-[:INTERESADO_EN]->(c)
        """, usuario=usuario["usuario"], categoria=categoria)

    for curso in usuario["cursos_realizados"]:
        tx.run("""
            MATCH (u:Usuario {usuario: $usuario}), (c:Curso {idCurso: $curso})
            MERGE (u)-[:REALIZÓ]->(c)
        """, usuario=usuario["usuario"], curso=curso)

    for curso in usuario.get("cursos_likeados", []):
        tx.run("""
            MATCH (u:Usuario {usuario: $usuario}), (c:Curso {idCurso: $curso})
            MERGE (u)-[:LIKEÓ]->(c)
        """, usuario=usuario["usuario"], curso=curso)

    for curso, rating in usuario.get("ratings", {}).items():
        tx.run("""
            MATCH (u:Usuario {usuario: $usuario}), (c:Curso {idCurso: $curso})
            MERGE (u)-[:CALIFICÓ {rating: $rating}]->(c)
        """, usuario=usuario["usuario"], curso=curso, rating=rating)

with driver.session() as session:
    with open("usuarios_simulados/usuarios.json", "r") as f:
        usuarios = json.load(f)
        for u in usuarios:
            session.write_transaction(cargar_usuarios, u)

driver.close()
