# registrar_interaccion.py

from algoritmo.utilidades_grafo import conectar_db

def registrar_interaccion(usuario, curso, tipo_interaccion, valor=None):
    """
    Registra una interacción de un usuario con un curso.
    tipo_interaccion: 'like', 'dislike', 'inscripcion', 'rating', 'completado'
    valor: solo aplica a 'rating', es la calificación (1-5)
    """
    db = conectar_db()
    query = ""

    if tipo_interaccion == "like":
        query = f'''
            MATCH (u:Usuario {{usuario: "{usuario}"}}), (c:Curso {{idCurso: "{curso}"}})
            MERGE (u)-[r:LIKE]->(c)
            ON CREATE SET r.peso = 1
            ON MATCH SET r.peso = r.peso + 1
        '''
    elif tipo_interaccion == "dislike":
        query = f'''
            MATCH (u:Usuario {{usuario: "{usuario}"}}), (c:Curso {{idCurso: "{curso}"}})
            MERGE (u)-[r:DISLIKE]->(c)
            ON CREATE SET r.peso = 1
            ON MATCH SET r.peso = r.peso + 1
        '''
    elif tipo_interaccion == "inscripcion":
        query = f'''
            MATCH (u:Usuario {{usuario: "{usuario}"}}), (c:Curso {{idCurso: "{curso}"}})
            MERGE (u)-[:INSCRITO_EN]->(c)
        '''
    elif tipo_interaccion == "completado":
        query = f'''
            MATCH (u:Usuario {{usuario: "{usuario}"}}), (c:Curso {{idCurso: "{curso}"}})
            MERGE (u)-[:COMPLETO]->(c)
            DELETE (u)-[:INSCRITO_EN]->(c)
        '''
    elif tipo_interaccion == "rating" and valor is not None:
        query = f'''
            MATCH (u:Usuario {{usuario: "{usuario}"}}), (c:Curso {{idCurso: "{curso}"}})
            MERGE (u)-[r:RATED]->(c)
            SET r.valor = {valor}
        '''

    if query:
        db.run(query)
