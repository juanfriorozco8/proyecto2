from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from neo4j import GraphDatabase
from dotenv import load_dotenv
import json
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASS = os.getenv("NEO4J_PASS")
app = Flask(__name__)
app.secret_key = 'supersecreto'
CORS(app)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def run_query(query, parameters=None, single=False):
    with driver.session() as session:
        result = session.run(query, parameters or {})
        if single:
            return result.single()
        else:
            return list(result)

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    usuario = data.get('usuario')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    intereses = data.get('intereses', [])

    q = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if run_query(q, {'usuario': usuario}, single=True):
        return jsonify({"error": "Usuario ya existe"}), 400

    query = """
    CREATE (u:Usuario {
        usuario:$usuario,
        correo:$correo,
        contrasena:$contrasena
    })
    """
    run_query(query, {'usuario': usuario, 'correo': correo, 'contrasena': contrasena})

    print("Intereses recibidos en backend:", intereses)
    for inter in intereses:
        # Crear etiqueta si no existe y relacionar
        q_inter = """
        MERGE (e:Etiqueta {nombre:$interes})
        WITH e
        MATCH (u:Usuario {usuario:$usuario})
        MERGE (u)-[:INTERESA_EN]->(e)
        """
        run_query(q_inter, {'usuario': usuario, 'interes': inter})

    return jsonify({"msg": "Usuario registrado exitosamente"})

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    q = "MATCH (u:Usuario {usuario:$usuario, contrasena:$contrasena}) RETURN u"
    record = run_query(q, {'usuario': usuario, 'contrasena': contrasena}, single=True)
    if record:
        session['usuario'] = usuario
        return jsonify({"msg": "Login exitoso"})
    else:
        return jsonify({"error": "Usuario o contraseña incorrecta"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/feed')
def feed_page():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    return render_template('feed.html', usuario=session['usuario'])

@app.route('/api/feed', methods=['POST'])
def api_feed():
    data = request.json
    usuario = data.get('usuario')
    if not usuario:
        return jsonify([])

    query = """
    MATCH (u:Usuario {usuario:$usuario})-[:INTERESA_EN]->(e:Etiqueta)<-[:ETIQUETA_DE]-(c:Curso)
    WHERE NOT (u)-[:INSCRITO_EN]->(c)
    RETURN c
    ORDER BY c.popularidad DESC, c.rating DESC
    LIMIT 10
    """

    result = run_query(query, {'usuario': usuario})

    cursos = []
    for record in result:
        c = record['c']
        cursos.append({
            "id": c.id,
            "titulo": c.get('titulo'),
            "categoria": c.get('categoria'),
            "duracion": c.get('duracion'),
            "dificultad": c.get('dificultad'),
            "foto": c.get('foto'),
            "rating": c.get('rating'),
        })

    return jsonify(cursos)

@app.route('/curso')
def curso_page():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    curso_id = request.args.get('id')
    if not curso_id:
        return "No se especificó curso", 400
    return render_template('curso.html', usuario=session['usuario'], curso_id=curso_id)

@app.route('/api/curso/<int:curso_id>', methods=['GET'])
def api_curso(curso_id):
    query = """
    MATCH (c:Curso)
    WHERE id(c) = $curso_id
    RETURN c
    """
    record = run_query(query, {'curso_id': curso_id}, single=True)
    if not record:
        return jsonify({"error": "Curso no encontrado"}), 404

    c = record['c']
    curso = {
        "id": curso_id,
        "titulo": c.get('titulo'),
        "categoria": c.get('categoria'),
        "duracion": c.get('duracion'),
        "dificultad": c.get('dificultad'),
        "contenido": c.get('contenido'),
        "foto": c.get('foto'),
        "autor": {
            "nombre": c.get('autor_nombre'),
            "bio": c.get('autor_bio'),
            "foto": c.get('autor_foto')
        }
    }
    return jsonify(curso)

@app.route('/api/inscribir', methods=['POST'])
def api_inscribir():
    data = request.json
    usuario = data.get('usuario')
    curso_id = data.get('curso_id')

    q_usuario = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if not run_query(q_usuario, {'usuario': usuario}, single=True):
        return jsonify({"error": "Usuario no encontrado"}), 404

    q_curso = "MATCH (c:Curso) WHERE id(c) = $curso_id RETURN c"
    if not run_query(q_curso, {'curso_id': int(curso_id)}, single=True):
        return jsonify({"error": "Curso no encontrado"}), 404

    q_inscribir = """
    MATCH (u:Usuario {usuario:$usuario}), (c:Curso)
    WHERE id(c) = $curso_id
    MERGE (u)-[:INSCRITO_EN]->(c)
    """
    run_query(q_inscribir, {'usuario': usuario, 'curso_id': int(curso_id)})

    return jsonify({"msg": "Inscripción exitosa"})

@app.route('/api/rating', methods=['POST'])
def api_rating():
    data = request.json
    usuario = data.get('usuario')
    curso_id = data.get('curso_id')
    rating = data.get('rating')

    q_usuario = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if not run_query(q_usuario, {'usuario': usuario}, single=True):
        return jsonify({"error": "Usuario no encontrado"}), 404

    q_curso = "MATCH (c:Curso) WHERE id(c) = $curso_id RETURN c"
    if not run_query(q_curso, {'curso_id': int(curso_id)}, single=True):
        return jsonify({"error": "Curso no encontrado"}), 404

    q_rating = """
    MATCH (c:Curso)
    WHERE id(c) = $curso_id
    SET c.rating = $rating
    """
    run_query(q_rating, {'curso_id': int(curso_id), 'rating': float(rating)})

    return jsonify({"msg": "Calificación guardada"})

@app.route('/cargar_base')
def cargar_base():
    with open('datos_base/autores.json', 'r', encoding='utf-8') as f:
        autores = json.load(f)

    with driver.session() as session:
        for autor in autores:
            session.run("""
            MERGE (a:Autor {nombre:$nombre})
            SET a.biografia=$bio, a.foto=$foto
            """, nombre=autor['nombre'], bio=autor.get('biografia',''), foto=autor.get('foto',''))

    etiquetas = ['Fotografía','Música','Diseño Gráfico','Programación','Cocina','Animación','Salud','Nutrición']
    with driver.session() as session:
        for e in etiquetas:
            session.run("MERGE (:Etiqueta {nombre:$nombre})", nombre=e)

    with open('datos_base/cursos.json', 'r', encoding='utf-8') as f:
        cursos = json.load(f)

    with driver.session() as session:
        for curso in cursos:
            print(f"Procesando curso: {curso['titulo']}, autor: {curso['autor']}")
            # 1. Crear o actualizar el nodo Curso
            session.run("""
                MERGE (c:Curso {titulo:$titulo})
                SET c.categoria=$categoria, c.dificultad=$dificultad, c.duracion=$duracion, c.contenido=$contenido,
                    c.foto=$foto, c.popularidad=0, c.rating=0
                """, titulo=curso['titulo'], categoria=curso['categoria'], dificultad=curso['dificultad'],
                    duracion=curso['duracion'], contenido=curso['contenido'], foto=curso.get('foto',''))
            
            # 2. Crear relación Autor -> Curso
            session.run("""
                MATCH (a:Autor {nombre:$autor}), (c:Curso {titulo:$titulo})
                MERGE (a)-[:AUTOR_DE]->(c)
                """, autor=curso['autor'], titulo=curso['titulo'])

            # 3. Crear relaciones Curso -> Etiqueta
            for etiqueta in curso.get('etiquetas', []):
                print(f"Relacionando curso '{curso['titulo']}' con etiqueta '{etiqueta}'")
                session.run("""
                    MATCH (c:Curso {titulo:$titulo}), (e:Etiqueta {nombre:$etiqueta})
                    MERGE (c)-[:ETIQUETA_DE]->(e)
                    """, titulo=curso['titulo'], etiqueta=etiqueta)


    return "Base cargada exitosamente"

if __name__ == '__main__':
    app.run(debug=True)
