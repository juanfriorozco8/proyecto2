from flask import Blueprint, request, jsonify
from backend.utils.neo4j_driver import get_driver

register_bp = Blueprint('register', __name__)
driver = get_driver()

# Endpoint: Registro de nuevo usuario
@register_bp.route('/register', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    username = data.get("usuario")
    contrasena = data.get("contrasena")
    correo = data.get("correo")
    intereses = data.get("intereses", [])  # lista de nombres de categorías

    if not username or not contrasena or not correo:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    with driver.session() as session:
        # Verifica si ya existe un usuario con ese username
        consulta_existencia = """
        MATCH (u:Usuario {usuario: $username})
        RETURN u
        """
        resultado = session.run(consulta_existencia, username=username)
        if resultado.single():
            return jsonify({"error": "El nombre de usuario ya existe"}), 409

        # Crea el nodo de usuario
        crear_usuario = """
        CREATE (u:Usuario {
            usuario: $username,
            contrasena: $contrasena,
            correo: $correo
        })
        """
        session.run(crear_usuario, username=username, contrasena=contrasena, correo=correo)

        # Crea relaciones de interés a categorías
        for categoria in intereses:
            relacion = """
            MATCH (u:Usuario {usuario: $username})
            MATCH (c:Categoria {nombre: $categoria})
            MERGE (u)-[:INTERESADO_EN]->(c)
            """
            session.run(relacion, username=username, categoria=categoria)

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

