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
    intereses = data.get("intereses", [])

    if not username or not contrasena or not correo:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    with driver.session() as session:
        # Verificar si el usuario ya existe
        existe_query = """
        MATCH (u:Usuario {usuario: $username})
        RETURN u
        """
        if session.run(existe_query, username=username).single():
            return jsonify({"error": "El nombre de usuario ya existe"}), 409

        # Crear el usuario
        crear_query = """
        CREATE (u:Usuario {
            usuario: $username,
            contrasena: $contrasena,
            correo: $correo
        })
        """
        session.run(crear_query, username=username, contrasena=contrasena, correo=correo)

        # Conectar usuario con categorías (insensible a capitalización)
        for categoria in intereses:
            relacion_query = """
            MATCH (u:Usuario {usuario: $username})
            MATCH (c:Categoria)
            WHERE toLower(c.nombre) = toLower($categoria)
            MERGE (u)-[:INTERESADO_EN]->(c)
            """
            session.run(relacion_query, username=username, categoria=categoria)

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


