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
    try:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            if single:
                return result.single()
            else:
                return list(result)
    except Exception as e:
        print(f"Neo4j query error: {str(e)}")
        raise

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
    session['usuario'] = usuario
    return jsonify({"msg": "Usuario registrado exitosamente", "redirect": "/intereses"})

@app.route('/intereses', methods=['GET'])
def intereses_page():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    return render_template('intereses.html')

@app.route('/api/intereses', methods=['POST'])
def cargar_intereses():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify({"error": "Sesión expirada o no iniciada"}), 403
    
    data = request.json
    intereses = data.get('intereses', [])
    
    if len(intereses) < 3:
        return jsonify({"error": "Debes seleccionar al menos 3 intereses"}), 400
    
    try:
        # Primero verificar que el usuario existe
        q_usuario = """
        MATCH (u:Usuario {usuario: $usuario})
        RETURN u
        """
        usuario_result = run_query(q_usuario, {'usuario': usuario})
        
        if not usuario_result:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # DEBUG: Verificar qué etiquetas existen en la base de datos
        q_todas_etiquetas = """
        MATCH (e:Etiqueta)
        OPTIONAL MATCH (e)-[:ETIQUETA_DE]->(c:Curso)
        RETURN e.nombre as etiqueta, COUNT(c) as cursos_disponibles
        ORDER BY e.nombre
        """
        todas_etiquetas = run_query(q_todas_etiquetas, {})
        print(f"DEBUG - Etiquetas disponibles en BD: {todas_etiquetas}")
        
        intereses_guardados = []
        intereses_no_encontrados = []
        debug_info = []
        
        for interes in intereses:
            print(f"DEBUG - Buscando interés: '{interes}'")
            
            # Buscar etiqueta que tenga relación con un curso
            q_buscar_etiqueta = """
            MATCH (e:Etiqueta {nombre: $interes})-[:ETIQUETA_DE]->(c:Curso)
            RETURN e.nombre as etiqueta, c.titulo as curso
            LIMIT 1
            """
            resultado_etiqueta = run_query(q_buscar_etiqueta, {'interes': interes})
            print(f"DEBUG - Resultado para '{interes}': {resultado_etiqueta}")
            
            if resultado_etiqueta:
                # Si existe la etiqueta con curso, crear la relación INTERESA_EN
                q_crear_interes = """
                MATCH (u:Usuario {usuario: $usuario})
                MATCH (e:Etiqueta {nombre: $interes})-[:ETIQUETA_DE]->(c:Curso)
                MERGE (u)-[:INTERESA_EN]->(e)
                RETURN e.nombre as etiqueta, c.titulo as curso
                """
                resultado_interes = run_query(q_crear_interes, {
                    'usuario': usuario, 
                    'interes': interes
                })
                
                if resultado_interes:
                    intereses_guardados.append({
                        'etiqueta': resultado_interes[0]['etiqueta'],
                        'curso': resultado_interes[0]['curso']
                    })
                    debug_info.append(f"✓ Guardado: {interes}")
                else:
                    debug_info.append(f"✗ Error al guardar: {interes}")
            else:
                # Verificar si la etiqueta existe pero sin cursos
                q_etiqueta_sin_curso = """
                MATCH (e:Etiqueta {nombre: $interes})
                RETURN e.nombre as etiqueta
                """
                etiqueta_existe = run_query(q_etiqueta_sin_curso, {'interes': interes})
                
                if etiqueta_existe:
                    debug_info.append(f"⚠ Etiqueta '{interes}' existe pero sin cursos")
                else:
                    debug_info.append(f"✗ Etiqueta '{interes}' no existe")
                
                intereses_no_encontrados.append(interes)
        
        print(f"DEBUG - Resumen: {debug_info}")
        
        # Si no se guardó ningún interés, intentar crear las etiquetas faltantes
        if len(intereses_guardados) == 0:
            print("DEBUG - No se guardaron intereses, intentando crear etiquetas...")
            
            # Crear etiquetas básicas si no existen
            etiquetas_basicas = [
                "Programación", "Diseño Gráfico", "Marketing Digital", 
                "Fotografía", "Música", "Idiomas", "Cocina", "Fitness", 
                "Negocios", "Arte", "Ciencia", "Tecnología"
            ]
            
            for etiqueta in etiquetas_basicas:
                if etiqueta in intereses:
                    # Crear la etiqueta y conectarla al usuario directamente
                    q_crear_etiqueta_directa = """
                    MERGE (e:Etiqueta {nombre: $etiqueta})
                    WITH e
                    MATCH (u:Usuario {usuario: $usuario})
                    MERGE (u)-[:INTERESA_EN]->(e)
                    RETURN e.nombre as etiqueta
                    """
                    resultado = run_query(q_crear_etiqueta_directa, {
                        'etiqueta': etiqueta,
                        'usuario': usuario
                    })
                    
                    if resultado:
                        intereses_guardados.append({
                            'etiqueta': etiqueta,
                            'curso': 'Curso general (se añadirán cursos específicos pronto)'
                        })
                        print(f"DEBUG - Creada etiqueta: {etiqueta}")
        
        # Verificar si se guardaron suficientes intereses
        if len(intereses_guardados) < 3:
            return jsonify({
                "error": f"Solo se pudieron guardar {len(intereses_guardados)} intereses válidos. Se requieren al menos 3.",
                "intereses_guardados": intereses_guardados,
                "intereses_no_encontrados": intereses_no_encontrados,
                "debug_info": debug_info,
                "etiquetas_disponibles": todas_etiquetas,
                "sugerencia": "Las etiquetas en la base de datos deben coincidir exactamente con los nombres seleccionados"
            }), 400
        
        return jsonify({
            "msg": "Intereses guardados exitosamente",
            "redirect": "/feed",
            "intereses_guardados": intereses_guardados,
            "intereses_no_encontrados": intereses_no_encontrados if intereses_no_encontrados else None,
            "debug_info": debug_info
        })
        
    except Exception as e:
        print(f"Error saving interests for user {usuario}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error al guardar los intereses: {str(e)}"}), 500


# Ruta adicional para crear etiquetas de prueba
@app.route('/api/crear-etiquetas-prueba', methods=['POST'])
def crear_etiquetas_prueba():
    """Ruta para crear etiquetas de prueba con cursos"""
    try:
        etiquetas_con_cursos = [
            {"etiqueta": "Programación", "curso": "Curso de Python Básico"},
            {"etiqueta": "Diseño Gráfico", "curso": "Curso de Photoshop"},
            {"etiqueta": "Marketing Digital", "curso": "Curso de Google Ads"},
            {"etiqueta": "Fotografía", "curso": "Curso de Fotografía Digital"},
            {"etiqueta": "Música", "curso": "Curso de Producción Musical"},
            {"etiqueta": "Idiomas", "curso": "Curso de Inglés Básico"},
            {"etiqueta": "Cocina", "curso": "Curso de Cocina Internacional"},
            {"etiqueta": "Fitness", "curso": "Curso de Entrenamiento Personal"},
            {"etiqueta": "Negocios", "curso": "Curso de Emprendimiento"},
            {"etiqueta": "Arte", "curso": "Curso de Pintura Básica"},
            {"etiqueta": "Ciencia", "curso": "Curso de Biología"},
            {"etiqueta": "Tecnología", "curso": "Curso de Redes y Sistemas"}
        ]
        
        for item in etiquetas_con_cursos:
            q_crear = """
            MERGE (c:Curso {titulo: $curso})
            MERGE (e:Etiqueta {nombre: $etiqueta})
            MERGE (e)-[:ETIQUETA_DE]->(c)
            RETURN e.nombre, c.titulo
            """
            run_query(q_crear, {
                'etiqueta': item['etiqueta'],
                'curso': item['curso']
            })
        
        return jsonify({"msg": "Etiquetas de prueba creadas exitosamente"})
        
    except Exception as e:
        return jsonify({"error": f"Error al crear etiquetas: {str(e)}"}), 500
        
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
        return jsonify({"msg": "Login exitoso", "redirect": "/intereses"})
    else:
        return jsonify({"error": "Usuario o contraseña incorrecta"}), 401

@app.route('/api/usuario', methods=['GET'])
def api_usuario():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify({"error": "No hay usuario en sesión"}), 403
    return jsonify({"usuario": usuario})

@app.route('/logout')

def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/feed')
def feed_page():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    return render_template('feed.html', usuario=session['usuario'])

@app.route('/api/categorias', methods=['GET'])
def api_categorias():
    query = """
    MATCH (e:Etiqueta)
    RETURN e.nombre AS categoria
    ORDER BY e.nombre
    """
    result = run_query(query)
    categorias = [record['categoria'] for record in result]
    return jsonify(categorias)

@app.route('/api/feed', methods=['POST'])
def api_feed():
    data = request.json
    usuario = data.get('usuario')
    categoria = data.get('categoria', '')
    orden = data.get('orden', 'compatibilidad')
    
    print(f"Usuario: {usuario}, Categoría: {categoria}, Orden: {orden}")
    
    if not usuario:
        print("Error: No se proporcionó usuario")
        return jsonify({"mis_cursos": [], "recomendados": [], "usuarios_similares": []})

    # Verificar usuario
    q_usuario = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if not run_query(q_usuario, {'usuario': usuario}, single=True):
        print(f"Error: Usuario {usuario} no encontrado")
        return jsonify({"mis_cursos": [], "recomendados": [], "usuarios_similares": []})

    # Obtener intereses (normalizados)
    q_intereses = """
    MATCH (u:Usuario {usuario:$usuario})-[:INTERESA_EN]->(e:Etiqueta)
    RETURN e.nombre AS etiqueta
    """
    intereses = [record['etiqueta'].strip().title() for record in run_query(q_intereses, {'usuario': usuario})]
    print(f"Intereses de {usuario}: {intereses}")

    # Obtener cursos inscritos (Mis cursos)
    q_mis_cursos = """
    MATCH (u:Usuario {usuario:$usuario})-[:INSCRITO_EN]->(c:Curso)
    """
    if categoria:
        q_mis_cursos += """
        MATCH (c)-[:ETIQUETA_DE]->(e:Etiqueta {nombre:$categoria})
        """
    q_mis_cursos += """
    RETURN c
    ORDER BY c.rating DESC
    LIMIT 50
    """
    mis_cursos_result = run_query(q_mis_cursos, {'usuario': usuario, 'categoria': categoria})
    mis_cursos = [{
        "id": c.element_id,
        "titulo": c.get('titulo'),
        "categoria": c.get('categoria'),
        "duracion": c.get('duracion'),
        "dificultad": c.get('dificultad'),
        "foto": c.get('foto'),
        "rating": c.get('rating', 0),
        "compatibilidad": 100.0,
        "inscrito": True
    } for c in [record['c'] for record in mis_cursos_result]]
    print(f"Mis cursos: {[curso['titulo'] for curso in mis_cursos]}")

    # Obtener autores preferidos (rating >= 4)
    q_autores_preferidos = """
    MATCH (u:Usuario {usuario:$usuario})-[r:CALIFICO]->(c:Curso)-[:AUTOR_DE]->(a:Autor)
    WHERE r.valor >= 4
    RETURN DISTINCT a.nombre AS autor
    """
    autores_preferidos = [record['autor'] for record in run_query(q_autores_preferidos, {'usuario': usuario})]
    print(f"Autores preferidos de {usuario}: {autores_preferidos}")

    # Obtener usuarios similares (similitud de Jaccard)
    q_usuarios_similares = """
    MATCH (u1:Usuario {usuario:$usuario})-[:INTERESA_EN]->(e1:Etiqueta)
    MATCH (u2:Usuario)-[:INTERESA_EN]->(e2:Etiqueta)
    WHERE u2 <> u1
    WITH u1, u2, collect(e1.nombre) AS intereses_u1, collect(e2.nombre) AS intereses_u2
    WITH u1, u2, intereses_u1, intereses_u2,
         size(intereses_u1) AS n1, size(intereses_u2) AS n2,
         size([x IN intereses_u1 WHERE x IN intereses_u2]) AS interseccion
    WHERE n1 > 0 AND n2 > 0
    RETURN u2.usuario AS usuario, interseccion * 1.0 / (n1 + n2 - interseccion) AS similitud
    ORDER BY similitud DESC
    LIMIT 5
    """
    usuarios_similares_result = run_query(q_usuarios_similares, {'usuario': usuario})
    usuarios_similares = [{
        "usuario": record['usuario'],
        "similitud": round(record['similitud'] * 100, 1)
    } for record in usuarios_similares_result]
    print(f"Usuarios similares a {usuario}: {[u['usuario'] for u in usuarios_similares]}")

    # Consulta para cursos recomendados
    query = """
    MATCH (u:Usuario {usuario:$usuario})
    // Cursos basados en intereses
    OPTIONAL MATCH (u)-[:INTERESA_EN]->(e:Etiqueta)<-[:ETIQUETA_DE]-(c1:Curso)
    WHERE NOT (u)-[:INSCRITO_EN]->(c1)
    // Cursos de autores preferidos
    OPTIONAL MATCH (c2:Curso)-[:AUTOR_DE]->(a:Autor)
    WHERE a.nombre IN $autores_preferidos AND NOT (u)-[:INSCRITO_EN]->(c2)
    // Cursos con alto rating
    OPTIONAL MATCH (c3:Curso)
    WHERE c3.rating >= 4 AND NOT (u)-[:INSCRITO_EN]->(c3)
    // Cursos tomados por usuarios similares
    OPTIONAL MATCH (c4:Curso)<-[:INSCRITO_EN]-(u2:Usuario)
    WHERE u2.usuario IN $usuarios_similares AND NOT (u)-[:INSCRITO_EN]->(c4)
    WITH collect(c1) + collect(c2) + collect(c3) + collect(c4) AS cursos, u
    UNWIND cursos AS c
    WITH DISTINCT c, u
    """
    if categoria:
        query += """
        MATCH (c)-[:ETIQUETA_DE]->(e2:Etiqueta {nombre:$categoria})
        """
    query += """
    OPTIONAL MATCH (c)-[:ETIQUETA_DE]->(e3:Etiqueta)
    OPTIONAL MATCH (c)-[:AUTOR_DE]->(a:Autor)
    OPTIONAL MATCH (c)<-[r:CALIFICO]-(u2:Usuario)
    WHERE u2.usuario IN $usuarios_similares
    WITH c, a, collect(e3.nombre) AS curso_etiquetas, collect(u2.usuario) AS usuarios_calificaron, avg(coalesce(r.valor, 0)) AS avg_rating_similares
    RETURN c, a.nombre AS autor_nombre, curso_etiquetas, avg_rating_similares
    """
    if orden == 'popularidad':
        query += " ORDER BY c.popularidad DESC, c.rating DESC"
    elif orden == 'rating':
        query += " ORDER BY c.rating DESC, avg_rating_similares DESC"
    else:  # compatibilidad
        query += " ORDER BY avg_rating_similares DESC, c.rating DESC"
    query += " LIMIT 50"

    result = run_query(query, {
        'usuario': usuario,
        'categoria': categoria,
        'autores_preferidos': autores_preferidos,
        'usuarios_similares': [u['usuario'] for u in usuarios_similares]
    })
    print(f"Cursos recomendados encontrados: {[record['c'].get('titulo') for record in result]}")

    recomendados = []
    for record in result:
        c = record['c']
        curso_etiquetas = [e.strip().title() for e in record['curso_etiquetas'] if e]
        print(f"Etiquetas de {c.get('titulo')}: {curso_etiquetas}")
        
        # Calcular compatibilidad
        coincidencias = len([e for e in curso_etiquetas if e in intereses])
        total_intereses = len(intereses) or 1
        compatibilidad = (coincidencias / total_intereses) * 100
        
        # Bonificaciones
        bonificacion_autor = 20 if record['autor_nombre'] in autores_preferidos else 0
        bonificacion_rating = 15 if c.get('rating', 0) >= 4 else 0
        bonificacion_similares = 10 if record['avg_rating_similares'] > 0 else 0
        compatibilidad = min(100, compatibilidad + bonificacion_autor + bonificacion_rating + bonificacion_similares)
        print(f"Compatibilidad de {c.get('titulo')}: {compatibilidad}% (coincidencias: {coincidencias}, total_intereses: {total_intereses})")

        # Razones de recomendación
        razones = []
        
        # Razón por coincidencia de intereses
        if coincidencias > 0:
            coincidencias_texto = ', '.join([e for e in curso_etiquetas if e in intereses])
            razones.append(f"Coincide con tus intereses: {coincidencias_texto}")
        
        # Razón por autor preferido
        if record['autor_nombre'] in autores_preferidos:
            razones.append(f"Creado por un autor que te gusta: {record['autor_nombre']}")
        
        # Razón por alta calificación
        if c.get('rating', 0) >= 4:
            razones.append("Curso con alta calificación general")
        
        # Razón por usuarios similares
        if record['avg_rating_similares'] > 0:
            razones.append("Tomado por usuarios con intereses similares")

        # **GARANTIZAR AL MENOS UNA RAZÓN**
        if not razones:
            # Si no hay razones específicas, agregar razones generales
            if c.get('rating', 0) >= 3:
                razones.append("Curso bien valorado por la comunidad")
            elif c.get('popularidad', 0) > 0:
                razones.append("Curso popular entre usuarios")
            elif categoria and c.get('categoria') == categoria:
                razones.append(f"Curso destacado en {categoria}")
            else:
                # Razón de último recurso - siempre válida
                razones.append("Curso recomendado para ampliar tus conocimientos")

        # **VALIDACIÓN FINAL: Asegurar que siempre hay al menos una razón**
        if not razones:
            razones.append("Curso sugerido para ti")

        # **FILTRAR CURSOS SIN RAZONES VÁLIDAS ANTES DE AGREGARLOS**
        # Solo agregar cursos que tengan al menos una razón de peso
        tiene_razon_valida = (
            coincidencias > 0 or  # Coincide con intereses
            record['autor_nombre'] in autores_preferidos or  # Autor preferido
            c.get('rating', 0) >= 3 or  # Rating decente
            record['avg_rating_similares'] > 0 or  # Usuarios similares
            c.get('popularidad', 0) > 0  # Tiene popularidad
        )
        
        # Si no tiene razón válida, skipear este curso
        if not tiene_razon_valida:
            print(f"Curso {c.get('titulo')} omitido por falta de razones válidas")
            continue

        recomendados.append({
            "id": c.element_id,
            "titulo": c.get('titulo'),
            "categoria": c.get('categoria'),
            "duracion": c.get('duracion'),
            "dificultad": c.get('dificultad'),
            "foto": c.get('foto'),
            "rating": c.get('rating', 0),
            "compatibilidad": round(compatibilidad, 1),
            "inscrito": False,
            "razones": [r for r in razones if r is not None]
        })

    recomendados = [{k: v for k, v in curso.items() if v is not None} for curso in recomendados]
    print(f"Cursos recomendados devueltos: {[curso['titulo'] for curso in recomendados]}")

    return jsonify({"mis_cursos": mis_cursos, "recomendados": recomendados, "usuarios_similares": usuarios_similares})

@app.route('/curso')
def curso_page():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    curso_id = request.args.get('id')
    if not curso_id:
        return "No se especificó curso", 400
    return render_template('curso.html', usuario=session['usuario'], curso_id=curso_id)

@app.route('/api/curso/<curso_id>', methods=['GET'])
def api_curso(curso_id):
    try:
        # Convertir curso_id a entero, extraer el último componente si es un element_id
        if ':' in curso_id:
            curso_id = int(curso_id.split(':')[-1])  # Tomar el último componente del element_id
        else:
            curso_id = int(curso_id)  # Convertir directamente si es un número

        query = """
        MATCH (c:Curso)
        WHERE id(c) = $curso_id
        OPTIONAL MATCH (c)-[:AUTOR_DE]->(a:Autor)
        RETURN c, a.nombre AS autor_nombre, a.biografia AS autor_bio, a.foto AS autor_foto
        """
        record = run_query(query, {'curso_id': curso_id}, single=True)
        if not record:
            return jsonify({"error": "Curso no encontrado"}), 404

        c = record['c']
        curso = {
            "id": c.element_id,  # Devolver element_id para mantener consistencia
            "titulo": c.get('titulo'),
            "categoria": c.get('categoria'),
            "duracion": c.get('duracion'),
            "dificultad": c.get('dificultad'),
            "contenido": c.get('contenido'),
            "foto": c.get('foto'),
            "autor": {
                "nombre": record.get('autor_nombre', ''),
                "bio": record.get('autor_bio', ''),
                "foto": record.get('autor_foto', '')
            }
        }
        return jsonify(curso)
    except ValueError:
        return jsonify({"error": "ID de curso inválido"}), 400
    except Exception as e:
        print(f"Error en api_curso: {str(e)}")
        return jsonify({"error": "Error al cargar el curso"}), 500

@app.route('/api/inscribir', methods=['POST'])
def api_inscribir():
    data = request.json
    usuario = data.get('usuario')
    curso_id = data.get('curso_id')

    if not usuario or not curso_id:
        return jsonify({"error": "Usuario o curso_id no proporcionado"}), 400

    q_usuario = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if not run_query(q_usuario, {'usuario': usuario}, single=True):
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        if ':' in curso_id:
            curso_id = int(curso_id.split(':')[-1])  
        else:
            curso_id = int(curso_id)  

        q_curso = "MATCH (c:Curso) WHERE id(c) = $curso_id RETURN c"
        if not run_query(q_curso, {'curso_id': curso_id}, single=True):
            return jsonify({"error": "Curso no encontrado"}), 404

        q_inscribir = """
        MATCH (u:Usuario {usuario:$usuario}), (c:Curso)
        WHERE id(c) = $curso_id
        MERGE (u)-[:INSCRITO_EN]->(c)
        SET c.popularidad = coalesce(c.popularidad, 0) + 1
        """
        run_query(q_inscribir, {'usuario': usuario, 'curso_id': curso_id})

        return jsonify({"msg": "Inscripción exitosa"})
    except ValueError:
        return jsonify({"error": "ID de curso inválido"}), 400
    except Exception as e:
        print(f"Error en api_inscribir: {str(e)}")
        return jsonify({"error": "Error al inscribirse"}), 500
    
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

    guardar_rating = """
    MERGE (u:Usuario {usuario:$usuario})
    WITH u
    MATCH (c:Curso) WHERE id(c) = $curso_id
    MERGE (u)-[r:CALIFICO]->(c)
    SET r.valor = $rating
    """
    run_query(guardar_rating, {
        'usuario': usuario,
        'curso_id': int(curso_id),
        'rating': float(rating)
    })

    actualizar_promedio = """
    MATCH (c:Curso) WHERE id(c) = $curso_id
    WITH c
    MATCH (u)-[r:CALIFICO]->(c)
    WITH c, avg(r.valor) AS promedio
    SET c.rating = promedio
    """
    run_query(actualizar_promedio, {'curso_id': int(curso_id)})

    return jsonify({"msg": "Calificación guardada y promedio actualizado"})

@app.route('/api/perfil_usuario', methods=['POST'])
def api_perfil_usuario():
    data = request.json
    usuario = data.get('usuario')
    
    if not usuario:
        return jsonify({"error": "No se proporcionó usuario"}), 400

    # Verificar usuario
    q_usuario = "MATCH (u:Usuario {usuario:$usuario}) RETURN u"
    if not run_query(q_usuario, {'usuario': usuario}, single=True):
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Obtener intereses
    q_intereses = """
    MATCH (u:Usuario {usuario:$usuario})-[:INTERESA_EN]->(e:Etiqueta)
    RETURN e.nombre AS interes
    """
    intereses = [record['interes'] for record in run_query(q_intereses, {'usuario': usuario})]

    # Obtener cursos inscritos y calificaciones
    q_cursos = """
    MATCH (u:Usuario {usuario:$usuario})-[:INSCRITO_EN]->(c:Curso)
    OPTIONAL MATCH (u)-[r:CALIFICO]->(c)
    RETURN c, r.valor AS calificacion
    """
    cursos_result = run_query(q_cursos, {'usuario': usuario})
    cursos = [{
        "id": c.element_id,
        "titulo": c.get('titulo'),
        "categoria": c.get('categoria'),
        "calificacion": record['calificacion'] if record['calificacion'] is not None else "Sin calificar"
    } for record in cursos_result for c in [record['c']]]

    return jsonify({
        "usuario": usuario,
        "intereses": intereses,
        "cursos": cursos
    })

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

    with open('datos_base/categorias.json', 'r', encoding='utf-8') as f:
        categorias_data = json.load(f)
    etiquetas = categorias_data['categorias']
    with driver.session() as session:
        for e in etiquetas:
            session.run("MERGE (:Etiqueta {nombre:$nombre})", nombre=e)
        for relacion in categorias_data['relaciones']:
            session.run("""
            MATCH (e1:Etiqueta {nombre:$desde}), (e2:Etiqueta {nombre:$hacia})
            MERGE (e1)-[:RELACIONADA {peso:$peso}]->(e2)
            """, **relacion)

    with open('datos_base/cursos.json', 'r', encoding='utf-8') as f:
        cursos = json.load(f)

    with driver.session() as session:
        for curso in cursos:
            curso_etiquetas = curso.get('etiquetas', [curso['categoria']])
            session.run("""
                MERGE (c:Curso {titulo:$titulo})
                SET c.categoria=$categoria, c.dificultad=$dificultad, c.duracion=$duracion, c.contenido=$contenido,
                    c.foto=$foto, c.popularidad=0, c.rating=0, c.etiquetas=$etiquetas
                """, titulo=curso['titulo'], categoria=curso['categoria'], dificultad=curso['dificultad'],
                    duracion=curso['duracion'], contenido=curso['contenido'], foto=curso.get('foto',''),
                    etiquetas=curso_etiquetas)
            
            session.run("""
                MATCH (a:Autor {nombre:$autor}), (c:Curso {titulo:$titulo})
                MERGE (a)-[:AUTOR_DE]->(c)
                """, autor=curso['autor'], titulo=curso['titulo'])

            for etiqueta in curso_etiquetas:
                session.run("""
                    MATCH (c:Curso {titulo:$titulo}), (e:Etiqueta {nombre:$etiqueta})
                    MERGE (c)-[:ETIQUETA_DE]->(e)
                    """, titulo=curso['titulo'], etiqueta=etiqueta)

    return "Base cargada exitosamente"

if __name__ == '__main__':
    app.run(debug=True)