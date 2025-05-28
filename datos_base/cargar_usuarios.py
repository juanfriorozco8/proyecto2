import json
from neo4j import GraphDatabase

# Configura tu conexión
URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def crear_usuario(tx, usuario):
    query = """
    MERGE (u:Usuario {idUsuario: $idUsuario})
    SET u.nombre = $nombre,
        u.email = $email,
        u.usuario = $usuario,
        u.contrasena = $contrasena
    """
    tx.run(query, **usuario)

def crear_relacion_interes(tx, idUsuario, interes):
    query = """
    MATCH (u:Usuario {idUsuario: $idUsuario})
    MATCH (c:Categoria {nombre: $interes})
    MERGE (u)-[:INTERESADO_EN]->(c)
    """
    tx.run(query, idUsuario=idUsuario, interes=interes)

def cargar_usuarios():
    with open("usuarios_simulados/usuarios.json", encoding="utf-8") as f:
        usuarios = json.load(f)

    with driver.session() as session:
        for usuario in usuarios:
            session.write_transaction(crear_usuario, usuario)
            for interes in usuario["intereses"]:
                session.write_transaction(crear_relacion_interes, usuario["idUsuario"], interes)

    print("✅ Usuarios cargados correctamente.")

if __name__ == "__main__":
    cargar_usuarios()
