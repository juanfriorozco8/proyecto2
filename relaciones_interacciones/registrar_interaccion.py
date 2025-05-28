import json
from algoritmo.utilidades_grafo import get_driver

def registrar_interacciones():
    driver = get_driver()
    with open("usuarios_simulados/usuarios.json", "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    with driver.session() as session:
        for usuario in usuarios:
            session.run(
                "MERGE (u:Usuario {username: $username, correo: $correo, contrasena: $contrasena})",
                username=usuario["username"],
                correo=usuario["correo"],
                contrasena=usuario["contrasena"]
            )
            for interes in usuario["intereses"]:
                session.run(
                    "MATCH (u:Usuario {username: $username}), (c:Categoria {nombre: $interes}) "
                    "MERGE (u)-[:INTERESADO_EN]->(c)",
                    username=usuario["username"],
                    interes=interes
                )

if __name__ == "__main__":
    registrar_interacciones()