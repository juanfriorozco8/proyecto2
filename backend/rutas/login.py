from flask import Blueprint, request, jsonify
from backend.utils.neo4j_driver import get_driver


login_bp = Blueprint('login', __name__)
driver = get_driver()

# Endpoint: Validar usuario y contraseña para login
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("usuario")
    password = data.get("contrasena")

    with driver.session() as session:
        query = """
        MATCH (u:Usuario {usuario: $username, contrasena: $password})
        RETURN u.usuario AS usuario
        """
        result = session.run(query, username=username, password=password)
        user = result.single()

        if user:
            return jsonify({"mensaje": "Login exitoso", "usuario": user["usuario"]}), 200
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
