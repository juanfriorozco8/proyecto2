import json
import os
from neo4j import GraphDatabase

# 🔐 Conexión a Aura (ajusta esto)
URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# 📁 Ruta absoluta a esta carpeta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🗂️ Rutas absolutas a los archivos JSON
AUTORES_PATH = os.path.join(BASE_DIR, "autores.json")
CURSOS_PATH = os.path.join(BASE_DIR, "cursos.json")

def cargar_datos():
    with open(AUTORES_PATH, encoding="utf-8") as f:
        autores = json.load(f)
    with open(CURSOS_PATH, encoding="utf-8") as f:
        cursos = json.load(f)

    with driver.session() as session:
        session.write_transaction(crear_categorias, cursos)
        session.write_transaction(crear_autores, autores)
        session.write_transaction(crear_cursos, cursos)

def crear_categorias(tx, cursos):
    categorias = set(c["categoria"] for c in cursos)
    for cat in categorias:
        print(f"🟢 Categoría: {cat}")
        tx.run("MERGE (:Categoria {nombre: $nombre})", nombre=cat)

def crear_autores(tx, autores):
    for a in autores:
        print(f"🧑 Autor: {a['nombre']}")
        tx.run("""
            MERGE (a:Autor {id: $id})
            SET a.nombre = $nombre, a.bio = $bio, a.foto = $foto
        """, **a)

def crear_cursos(tx, cursos):
    for c in cursos:
        print(f"📘 Curso: {c['titulo']}")
        tx.run("""
            MERGE (c:Curso {id: $id})
            SET c.titulo = $titulo, c.dificultad = $dificultad, c.duracion = $duracion,
                c.contenido = $contenido, c.foto = $foto
            MERGE (cat:Categoria {nombre: $categoria})
            MERGE (c)-[:PERTENECE_A]->(cat)
            MERGE (a:Autor {id: $autor_id})
            MERGE (a)-[:IMPARTE]->(c)
        """, **c)

if __name__ == "__main__":
    print("🚀 Iniciando carga...")
    cargar_datos()
    print("✅ ¡Todo cargado en Neo4j!")


